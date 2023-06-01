from django.shortcuts import render, redirect
from django.urls import reverse

from ..cart.services import CartService
from .forms import OrderCreateForm
from .service import OrderService


def create_order(request):
    cart = CartService.get_cart(request)
    if request.method == 'POST':
        form, order = OrderService.create_order(request, cart)
        # set the order in the session
        request.session['order_id'] = order.id
        # redirect for payment
        return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'orders/create_order.html', context)
