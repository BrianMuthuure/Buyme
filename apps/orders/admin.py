from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f"<a href='{url}' target='_blank'>{obj.stripe_id}</a>"
        return mark_safe(html)
    return ''


order_payment.short_description = 'Stripe Payment'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'first_name', 'last_name', 'email', 'address',
        'postal_code', 'city', order_payment,  'created_at', 'updated_at', 'is_paid']
    list_filter = ['is_paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
