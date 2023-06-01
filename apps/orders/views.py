from django.shortcuts import render
from ..cart.services import CartService
from .forms import OrderCreateForm
from .service import OrderService


def create_order(request):
    cart = CartService.get_cart(request)
    if request.method == 'POST':
        form, order = OrderService.create_order(request, cart)
        return render(request, 'orders/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'orders/create_order.html', context)

