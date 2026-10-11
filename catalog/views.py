from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category
from django.views.generic import ListView, DetailView


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


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо {name}! Сообщение успешно отправлено. \n <a href='/'>Каталог</a>")

    return render(request, 'contacts.html')


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'product.html', {'product':product})
