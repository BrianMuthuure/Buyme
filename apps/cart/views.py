from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from apps.cart.services import CartService


@require_POST
def cart_add(request, product_id):
    CartService.add_to_cart(request, product_id)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    CartService.remove_from_cart(request, product_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = CartService.get_cart(request)
    # allow the user to update the quantity of a product in the cart
    CartService.update_cart(cart)
    return render(request, 'cart/detail.html', {'cart': cart})
