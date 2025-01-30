from datetime import date
from os import name
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

# Define a Profile model to extend the built-in User model with additional information
class Profile(models.Model):
    # One-to-One relationship with the User model: each user can have only one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)  
    phone = models.CharField(max_length=10, null=True,blank=True)  # User's phone number (optional)
    address1 = models.CharField(max_length=50, null=True, blank=True)  # First line of address (optional)
    address2 = models.CharField(max_length=50, null=True, blank=True)  # Second line of address (optional)
    city = models.CharField(max_length=50, null=True, blank=True)  # User's city (optional)
    state = models.CharField(max_length=50, null=True, blank=True)  # User's state (optional)
    # country = models.CharField(max_length=50, null=True, blank=True)  # User's country (optional)
    pincode = models.CharField(max_length=50, null=True, blank=True)  # Postal code (optional)
    old_cart = models.CharField(max_length=200, blank =True)

    def __str__(self):
        # Return the username associated with this profile when printed
        return self.user.username

# Signal handler function to automatically create a Profile instance when a new User is created
def create_profile(sender, instance, created, **kwargs):
    """
    Create a Profile instance automatically when a new User instance is created.
    Args:
        sender: The model class that sent the signal (User).
        instance: The actual instance of the User model that was created.
        created: A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        # Create a new Profile instance linked to the newly created User instance
        user_profile = Profile(user=instance)
        user_profile.save()  # Save the new Profile instance to the database

# Connect the create_profile function to the post_save signal of the User model
post_save.connect(create_profile, sender=User)

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
    
