from django.db.models import Model, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category
from catalog.forms import ContactForm
from django.views.generic import ListView, DetailView, TemplateView, FormView


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        # если приходит slug из get-запроса
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            return category.products.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            context['category'] = get_object_or_404(Category, slug=slug)
            context['all_products'] = False
        else:
            context['category'] = 'Все товары'
            context['all_products'] = True
        return context


class ProductDetailView(DetailView):
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