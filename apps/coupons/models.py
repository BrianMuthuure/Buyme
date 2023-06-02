from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        help_text='Discount in percentage',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField()

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return self.code
