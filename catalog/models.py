from decimal import Decimal
from django.utils.text import slugify

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование', help_text='Введите название Категории',
                            db_index=True)
    slug = models.SlugField(blank=True, verbose_name='slug', help_text='Автоматически заполняется из названия')

    description = models.TextField(verbose_name='Описание', help_text='Описание Категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование', help_text='Введите название Продукта',db_index=True)
    description = models.TextField(verbose_name='Описание', help_text='Описание Продукта')

    photo = models.ImageField(upload_to='catalog/photo/products', blank=True, null=True, verbose_name='Фотография', help_text='Загрузите фото продукта')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', help_text='Введите цену', default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.name}> из категории < {self.category} > "

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['price', 'name']

# class User(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя Пользователя',
#                             db_index=True)
#     photo = models.ImageField(upload_to='catalog/photo/users', blank=True, null=True, verbose_name='Фотография', help_text='Загрузите фото')
#
#     phone = models.CharField(max_length=12, verbose_name='Телефон', help_text='Введите номер телефона',db_index=True)
#     country = models.CharField(max_length=255, verbose_name='Страна', help_text='Введите название страны',db_index=True)
#     address = models.CharField(max_length=255, verbose_name='Адрес', help_text='Введите Адрес',db_index=True)
