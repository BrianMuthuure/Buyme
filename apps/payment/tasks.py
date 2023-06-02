from io import BytesIO

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.orders.models import Order


class StripePaymentHandler:
    @staticmethod
    @shared_task
    def send_payment_success_email(order_id):
        """
        Task to send an e-mail notification when an order is successfully paid.
        """
        try:
            order = Order.objects.get(id=order_id)
            subject = f"BuyMe Smart Shop - Invoice no. {order.order_id}"
            message = "Please, find attached the invoice for your recent purchase."
            email = EmailMessage(subject, message, "admin@buymesmartshop.com", [order.email])
            html = render_to_string('orders/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            email.attach(f"order_{order.order_id}.pdf", out.getvalue(), "application/pdf")
            email.send()
            return True
        except Exception as e:
            print(e)
            return False
