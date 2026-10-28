from config.settings import CACHE_ENABLED
from catalog.models import Product, Category
from django.core.cache import cache
from django.shortcuts import get_object_or_404


class ProductService:
    @staticmethod
    def get_products_from_cache(category_slug=None, timeout=60 * 15):
        """
        Возвращает список продуктов для категории (по slug) или все товары.
        Использует кэш с ключом, зависящим от slug.
        """
        if not CACHE_ENABLED:
            return

        # 1. Формируем ключ
        if category_slug:
            cache_key = f"products_category_{category_slug}"
        else:
            cache_key = "products_category_items"

        # 2. Сначала пробуем взять из кэша
        cached_data = cache.get(cache_key)

        if cached_data is None:
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                qs = category.products.all()
            else:
                category = None
                qs = Product.objects.all()

            products = list(qs)

            # Сохраняем в кэш: кортеж (список продуктов, категория)
            cache.set(cache_key, (products, category), timeout)
            return products, category

        if not isinstance(cached_data, tuple) or len(cached_data) != 2:
            # Если формат нарушен (например, кэш битый) — пересоздадим
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                qs = category.products.all()
            else:
                category = None
                qs = Product.objects.all()

            products = list(qs)
            cache.set(cache_key, (products, category), timeout)
            return products, category

        products, category = cached_data
        return products, category


