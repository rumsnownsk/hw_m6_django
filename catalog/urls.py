from django.urls import path, include

from catalog.views import ProductListView
from catalog.apps import CatalogConfig
from . import views  # <--- ЭТОЙ СТРОКИ НЕ ХВАТАЕТ
app_name = CatalogConfig.name

urlpatterns = [
    # path('', views.index, name='main'),

    # path('<slug:slug>/', views.index, name='main_with_select_category'),
    # path('products/<int:pk>/', views.product_detail, name='product_detail'),


    # Главная: все товары
    path('', ProductListView.as_view(), name='products_list'),

    # Категория: товары по слагу
    path('<slug:slug>/', views.ProductListView.as_view(), name='products_list_by_category'),

    # Отображение одного продукта
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

]
