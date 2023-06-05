from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from ..cart.services import CartService
from ..coupons.forms import CouponApplyForm
from ..products.recommender import Recommender


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
    coupon_apply_form = CouponApplyForm()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = Recommender().suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []
    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'recommended_products': recommended_products
    }
    return render(request, 'cart/detail.html', context)
