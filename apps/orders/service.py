from .forms import OrderCreateForm
from .models import OrderItem, Order
from ..notifications.tasks import EmailHandler


class OrderService:

    @staticmethod
    def create_order(request, cart):
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
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
        order.paid = True
        order.stripe_id = stripe_id
        order.save()

        # launch asynchronous task

        return order
