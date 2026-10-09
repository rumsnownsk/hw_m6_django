from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category


def index(request, slug=None):
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.all()
    else:
        products = Product.objects.all()
        category = 'Все товары:'
    return render(request, 'main.html', {
        'category': category,
        'products': products,
        'all_products': True if not slug else False
    })


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо {name}! Сообщение успешно отправлено. \n <a href='/'>Каталог</a>")

    return render(request, 'contacts.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product':product})
