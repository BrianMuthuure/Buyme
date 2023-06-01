from django.shortcuts import render, get_object_or_404

from .models import Category
from .services import ProductService
from ..cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = ProductService.get_all_categories()
    products = ProductService.get_all_products()
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'products/list.html', context)


def product_detail(request, id, slug):
    product = ProductService.get_product_by_id_and_slug(id, slug)
    cart_product_form = CartAddProductForm()
    context = {
        "product": product,
        "cart_product_form": cart_product_form
    }
    return render(request, 'products/details.html', context)
