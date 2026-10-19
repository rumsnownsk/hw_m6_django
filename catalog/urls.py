from django.urls import path, include

from catalog.views import ProductListView
from catalog.apps import CatalogConfig
from . import views
app_name = CatalogConfig.name

urlpatterns = [
    # Главная: все товары
    path('', ProductListView.as_view(), name='products_list'),

    # Страница Контакты
    path('contacts/', views.ContactView.as_view(), name='contacts'),

    # Категория: товары по слагу
    path('<slug:slug>/', views.ProductListView.as_view(), name='products_list_by_category'),

    # Отображение одного продукта
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Форма создания продукта
    path('product/create', views.ProductCreateView.as_view(), name='product_create'),

    # Форма редактирования продукта по ID
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product_update'),

    # Форма удаления продукта по ID
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
]
