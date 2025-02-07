from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.payment_success , name='payment_success'),
    path('shipping_details/', views.shipping_details , name = 'shipping_details'),
    path('checkout', views.checkout , name = 'checkout'),
    ]
