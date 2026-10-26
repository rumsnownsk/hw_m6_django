import os
import uuid
from django.forms import ValidationError

from transliterate import translit


def translit_image(instance, filename):
    """
    Генерирует имя файла для картинки поста:
    - транслитерирует имя (кириллица → латиница)
    - убирает лишние спецсимволы
    - возвращает путь blog_previews/<имя><расширение>
    """
    name, ext = os.path.splitext(filename)

    # translit(name, 'ru') превращает кириллицу в латиницу
    # reversed=True убирает диакритику и делает чистый ASCII
    new_name = translit(instance.name, 'ru', reversed=True)

    # Оставляем только буквы, цифры и дефисы, остальное заменяем на '-'
    # Это защитит от странных символов в именах файлов
    import re
    new_name = re.sub(r'[^a-z0-9\-]+', '-', new_name.lower()).strip('-')

    unique_suffix = uuid.uuid4().hex[:6]

    return f'catalog/photo/products/{new_name}_{unique_suffix}{ext}'


def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            f"Файл слишком большой. Максимальный размер: 5 МБ. Текущий: {value.size / 1024 / 1024:.2f} МБ")
