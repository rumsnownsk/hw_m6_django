from django.contrib import admin
from django.utils.html import format_html

from catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo_tag', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;"/>',
                obj.photo.url
            )
        return "Нет фото"
    # Опционально: делаем заголовок колонки понятным
    photo_tag.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'description')
