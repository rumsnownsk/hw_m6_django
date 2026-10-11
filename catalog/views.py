from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо {name}! Сообщение успешно отправлено. \n <a href='/'>Каталог</a>")

    return render(request, 'contacts.html')


def home(request):
    last_five_products = Product.objects.order_by('-created_at', '-id')[:5]
    for p in last_five_products:
        print(p)
    return render(request, 'home.html', {
        'last_five_products': last_five_products
    })
