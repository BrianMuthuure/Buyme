from django.shortcuts import render
from .services import ProductService


def product_list(request, category_slug=None):
    category = None
    categories = ProductService.get_all_categories()
    products = ProductService.get_all_products()
    if category_slug:
        category, products = ProductService.get_products_by_category(category_slug)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'products/list.html', context)


def product_detail(request, id, slug):
    product = ProductService.get_product_by_id_and_slug(id, slug)
    context = {
        "product": product,
    }
    return render(request, 'products/details.html', context)
