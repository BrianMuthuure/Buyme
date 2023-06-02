from  decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ..coupons.models import Coupon
from ..products.models import Product
from .utils import generate_order_id


class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)
    coupon = models.ForeignKey(
        Coupon, related_name='orders',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, blank=True, null=True,
        help_text='Coupon discount in percent',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Order {self.order_id}'

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"Order-{generate_order_id()}"
        return super().save(*args, **kwargs)

    def get_total_cost_before_discount(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test mode
            path = '/test/'
        else:
            # Stripe path for live mode
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity
