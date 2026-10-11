from .models import Category

def categories(request):
    """Возвращает словарь со всеми категориями для любого шаблона"""
    return {'categories': Category.objects.all()}