from django.contrib import admin
from .models import ShippingAddress, OrderItem, Order

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['fullname', 'email', 'shipping_address','date_ordered','shipped','date_shipped']

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)