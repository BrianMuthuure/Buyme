from _decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse

from apps.payment.models import Payment

# create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class StripePaymentService:

    @staticmethod
    def charge(request, order):
        try:
            success_url = request.build_absolute_uri(reverse('payment:completed'))
            cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
            # stripe checkout session data
            data = {
                'mode': 'payment', 'client_reference_id': order.id,
                'success_url': success_url, 'cancel_url': cancel_url,
                'line_items': []
            }
            # add line items to the session data
            for item in order.items.all():
                data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                })
            # create stripe checkout session
            session = stripe.checkout.Session.create(**data)
            return session
        except Exception as e:
            raise e

    @staticmethod
    def create_payment_object(order):
        try:
            Payment.objects.create(
                email=order.email,
                amount=order.get_total_cost(),
                stripe_charge_id=order.stripe_id,
                order_id=order.order_id

            )
            return True
        except Exception as e:
            print(e)
            return False
