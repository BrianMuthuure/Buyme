import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
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


@staff_member_required
def admin_order_detail(request, order_id):
    order = OrderService.get_order_by_id(order_id)
    html = render_to_string('orders/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
    return response
