from datetime import date
from os import name
from tabnanny import verbose
from django.db import models

# Create your models here.

# customer
class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.firstname + ' ' + self.lastname

# product category
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'


# all the products
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(default = 0, decimal_places = 2, max_digits=9)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, null = True)
    def __str__(self):
        return self.name

# customer orders
class Order(models.Model):
    product= models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    date = models.DateField(default = date.today)
    status = models.BooleanField(default = False)
    
    def __str__(self):
        return self.product + ' - ' + str(self.quantity)
    
