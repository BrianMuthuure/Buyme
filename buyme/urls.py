from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include("apps.cart.urls", namespace="cart")),
    path('orders/', include("apps.orders.urls", namespace="orders")),
    path('payment/', include("apps.payment.urls", namespace="payment")),
    path('coupons/', include("apps.coupons.urls", namespace="coupons")),
    path('', include("apps.products.urls", namespace="products")),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
