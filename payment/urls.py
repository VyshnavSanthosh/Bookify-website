from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.payment_success , name='payment_success'),
    path('shipping_details/', views.shipping_details , name = 'shipping_details'),
    path('checkout', views.checkout , name = 'checkout'),
    path('process_order', views.process_order , name = 'process_order'),
    path('unshipped_dashboard',  views.unshipped_dashboard , name = 'unshipped_dashboard'),
    path('shipped_dashboard',  views.shipped_dashboard , name = 'shipped_dashboard'),
    path('order_details/<int:pk>', views.order_details , name = 'order_details'),
    ]
