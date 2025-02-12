from django.db import models
from django.contrib.auth.models import User
from django.db import models
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import  receiver
import datetime
# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_fullname = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=100)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, null=True, blank=True)
    shipping_state = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50)
    shipping_pincode = models.CharField(max_length=50)

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, *args, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        # obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped:
            instance.date_shipped = now

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'order  item - {str(self.id)}'

