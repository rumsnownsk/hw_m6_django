from django.db.models import Model, F
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category, Supplier
from catalog.forms import ContactForm, ProductForm, SupplierForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView, UpdateView, DeleteView


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    # paginate_by = 4

    def get_queryset(self):
        # если приходит slug из get-запроса
        slug = self.kwargs.get('slug')
        if slug:
            self.category = get_object_or_404(Category, slug=slug)
            return self.category.products.all()
        self.category = None
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.category:
            context['category'] = self.category
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')

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