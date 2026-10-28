from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Model, F
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category, Supplier
from catalog.forms import ContactForm, ProductForm, SupplierForm, ProductModeratorForm
from catalog.services import ProductService
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .mixins import RedirectToHomeMixin


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    # paginate_by = 4

    def get_queryset(self):
        # если приходит slug из get-запроса
        slug = self.kwargs.get('slug')

        products, category = ProductService.get_products_from_cache(slug)
        self.category = category
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.category:
            context['category'] = self.category
            context['all_products'] = False
        else:
            context['category'] = 'Все товары'
            context['all_products'] = True
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(RedirectToHomeMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'  # в шаблоне будет переменная product, а не object

    def get_object(self, queryset = None):
        obj = super().get_object(queryset=queryset)

        # Атомарно увеличиваем views в базе: views = views + 1
        Product.objects.filter(pk=obj.pk).update(views=F('views') + 1)

        # Возвращаем объект для шаблона.
        # Важно: после update() значение в obj не обновится автоматически,
        # поэтому лучше взять свежий объект из базы.
        return Product.objects.get(pk=obj.pk)


class ProductCreateView(RedirectToHomeMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, RedirectToHomeMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, RedirectToHomeMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')

    def dispatch(self, request, *args, **kwargs):
        # Сначала загружаем объект (чтобы он был в self.object)
        response = super().dispatch(request, *args, **kwargs)

        # Если объект не найден (404) — просто возвращаем ответ, дальше не проверяем
        if not hasattr(self, 'object') or self.object is None:
            return response

        user = request.user
        obj = self.object

        # 1. Если у пользователя есть право на удаление продуктов — разрешаем
        if user.has_perm('catalog.delete_product'):
            return response

        # 2. Иначе проверяем, что пользователь — владелец этого продукта
        if obj.owner_id == user.id:
            return response

        # Ни одно условие не подошло — запрещаем
        raise PermissionDenied("Вы не можете удалять этот продукт")

class ContactView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = '/'  # куда редиректить после отправки

    def form_valid(self, form):

        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data.get('message', '')

        # Тут можно сохранить в БД или отправить на почту
        # Например: Contact.objects.create(name=name, phone=phone, message=message)

        return super().form_valid(form)