from .forms import OrderCreateForm
from .models import OrderItem
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
