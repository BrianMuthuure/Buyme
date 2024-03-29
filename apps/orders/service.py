from .forms import OrderCreateForm
from .models import OrderItem, Order
from ..notifications.tasks import EmailHandler
from ..payment.service import StripePaymentService
from ..payment.tasks import StripePaymentHandler


class OrderService:

    @staticmethod
    def create_order(request, cart):
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderService.create_order_item(order, item)
            cart.clear()

            # send email notification to the customer
            EmailHandler.send_complete_order_email.delay(order.id)
            return form, order

    @staticmethod
    def create_order_item(order, item):
        order_item = OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity'])
        return order_item

    @staticmethod
    def get_order_by_id(order_id):
        return Order.objects.get(id=order_id)

    @staticmethod
    def mark_order_as_paid(order_id, stripe_id):
        order = OrderService.get_order_by_id(order_id)
        order.is_paid = True
        order.stripe_id = stripe_id
        order.save()
        StripePaymentService.create_payment_object(order)
        # launch asynchronous task
        StripePaymentHandler.send_payment_success_email.delay(order.id)
        return order
