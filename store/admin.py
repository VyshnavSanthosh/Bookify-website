from django.contrib import admin
from .models import Product, Category, Customer, Order, Profile
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]
admin.site.register(Profile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)  