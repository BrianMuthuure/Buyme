from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .service import CouponService


@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        CouponService.apply_coupon_to_cart(request, form)
    return redirect('cart:cart_detail')

