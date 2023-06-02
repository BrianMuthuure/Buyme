from django.utils import timezone

from apps.coupons.models import Coupon


class CouponService:

    @staticmethod
    def get_coupon_by_code(code):
        return Coupon.objects.get(code=code, active=True)

    @staticmethod
    def get_a_specific_coupon(code, now):
        return Coupon.objects.get(
            code__iexact=code,
            valid_from__lte=now, valid_to__gte=now, active=True)

    @staticmethod
    def apply_coupon_to_cart(request, form):
        try:
            now = timezone.now()
            code = form.cleaned_data['code']
            coupon = CouponService.get_a_specific_coupon(code, now)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

        return request.session['coupon_id']
