from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('email', 'stripe_charge_id', 'order_id', 'amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('email', 'stripe_charge_id', 'order_id')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)