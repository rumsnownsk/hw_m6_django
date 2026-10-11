from django.urls import path, include

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.index, name='main'),

    path('<slug:slug>/', views.index, name='main_with_select_category'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

]
