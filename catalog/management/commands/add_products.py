from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Добавление Продуктов в базу данных"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        # загрузка данных из файла фикстур
        call_command('loaddata', 'catalog_data.json')

        # загрузка данных, типа, в ручную
        category, _ = Category.objects.get_or_create(name='Стройматериалы', description='Они нужны чтобы строить будущее')

        products = [
            {'name': 'Кирпич', 'description': 'красный прямоугольный с дырками', 'category': category},
            {'name': 'Труба', 'description': 'Дымовая длинная нержавеющая', 'category': category},
            {'name': 'Ламинат', 'description': 'Водостойкий крепкий надёжный', 'category': category},
        ]

        for p in products:
            product, created = Product.objects.get_or_create(**p)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Продукт <{product}> добавлен в категорию <{category}>'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт <{product}> уже имеется в БД'))
