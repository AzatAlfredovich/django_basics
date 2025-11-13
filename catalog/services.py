from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Получает данные о продуктах из кэша, или из БД, если кэш пуст"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_products_by_category(category_id):
    """
    Возвращает список всех продуктов в заданной категории по её ID
    """
    try:
        category = Category.objects.get(pk=category_id)
        products = Product.objects.filter(category=category).order_by("name")
        return products
    except Category.DoesNotExist:
        return []
