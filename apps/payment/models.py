from django.db import models


class Payment(models.Model):
    email = models.EmailField(blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ('-created_at',)

    def __str__(self):
        return self.stripe_charge_id
