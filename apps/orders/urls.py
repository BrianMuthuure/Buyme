from django.urls import path
from .views import create_order, admin_order_detail

app_name = 'orders'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', admin_order_detail, name='admin_order_pdf')
]
