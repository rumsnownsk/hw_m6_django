import os
from transliterate import translit

def blog_image_upload(instance, filename):
    """
    Генерирует имя файла для картинки поста:
    - транслитерирует имя (кириллица → латиница)
    - убирает лишние спецсимволы
    - возвращает путь blog_previews/<имя><расширение>
    """
    name, extension = os.path.splitext(filename)

    # translit(name, 'ru') превращает кириллицу в латиницу
    # reversed=True убирает диакритику и делает чистый ASCII
    new_name = translit(name, 'ru', reversed=True)

    # Оставляем только буквы, цифры и дефисы, остальное заменяем на '-'
    # Это защитит от странных символов в именах файлов
    import re
    new_name = re.sub(r'[^a-z0-9\-]+', '-', new_name.lower()).strip('-')

    return f'blog_previews/{new_name}{extension}'