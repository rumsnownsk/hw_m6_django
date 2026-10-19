import os.path
from decimal import Decimal

from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from .utils import translit_image, validate_file_size
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите название Категории",
        db_index=True,
    )
    slug = models.SlugField(
        blank=True,
        verbose_name="slug",
        help_text="Автоматически заполняется из названия",
    )

    description = models.TextField(
        verbose_name="Описание", help_text="Описание Категории"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Supplier(models.Model):
    name = models.CharField("Название поставщика", max_length=255)
    contact_name = models.CharField("Контактное лицо", max_length=100, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)
    website = models.URLField("Сайт", blank=True)
    address = models.TextField("Адрес", blank=True)
    notes = models.TextField(
        "Примечания", blank=True, help_text="Условия работы, сроки, особенности и т.п."
    )
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="Введите название Продукта",
        db_index=True,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Описание Продукта"
    )

    photo = models.ImageField(
        upload_to=translit_image,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size,
        ],
        blank=True,
        null=True,
        verbose_name="Фотография",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену",
        default=Decimal("0.00"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # добавляем поле для счётчика
    views = models.PositiveIntegerField(default=0)

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,  # если поставщика удалят, у продукта будет NULL
        null=True,  # можно оставить без поставщика временно
        blank=True,  # в админке можно не заполнять
        related_name="products",  # через supplier.products получишь все товары поставщика
        verbose_name="Поставщик",
    )

    def __str__(self):
        return f"<{self.name}> из категории < {self.category} > "

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
                if (
                    old_instance.photo
                    and self.photo
                    and old_instance.photo.name != self.photo.name
                ):
                    if os.path.isfile(old_instance.photo.path):
                        os.remove(old_instance.photo.path)
                elif old_instance.photo and not self.photo:
                    old_path = old_instance.photo.path
                    if os.path.exists(old_path):
                        os.remove(old_path)
            except Product.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["price", "name"]




# class User(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя Пользователя',
#                             db_index=True)
#     photo = models.ImageField(upload_to='catalog/photo/users', blank=True, null=True, verbose_name='Фотография', help_text='Загрузите фото')
#
#     phone = models.CharField(max_length=12, verbose_name='Телефон', help_text='Введите номер телефона',db_index=True)
#     country = models.CharField(max_length=255, verbose_name='Страна', help_text='Введите название страны',db_index=True)
#     address = models.CharField(max_length=255, verbose_name='Адрес', help_text='Введите Адрес',db_index=True)
