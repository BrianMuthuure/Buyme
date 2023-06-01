from django.shortcuts import redirect, render

from apps.orders.service import OrderService
from apps.payment.service import StripePaymentService


def payment_process(request):
    try:
        order_id = request.session.get('order_id', None)
        order = OrderService.get_order_by_id(order_id)
        if request.method == 'POST':
            session = StripePaymentService.charge(request, order)
            return redirect(session.url, code=303)
        else:
            return render(request, 'payment/process.html', locals())
    except Exception as e:
        raise e


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')