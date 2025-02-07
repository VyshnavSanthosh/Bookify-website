from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import ShippingAddress
from .forms import ShippingForm, PaymentForm

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')



def shipping_details(request):
    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            form = ShippingForm(request.POST or None)  # Create a new form if no address exists
            messages.warning(request, 'No shipping address found. Please fill out the form.')
    else:
        form = ShippingForm()

    if request.method == 'POST':
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Associate the address with the user
            shipping_address.save()
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'payment/shipping_details.html', {'form': form})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    cart_total_price = cart.get_total_price()
    cart_quantity = cart.get_total_quantity()
    
    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            form = ShippingForm(request.POST or None, instance=shipping_user)
            payment_form = PaymentForm(request.POST or None )
        except ShippingAddress.DoesNotExist:
            form = ShippingForm(request.POST or None)  # Create a new form if no address exists
            payment_form = PaymentForm(request.POST or None)  # Create a new form if no address exists

    else:
        form = ShippingForm()
        payment_form = PaymentForm()

    if request.POST:
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user  # Associate the address with the user
            shipping_address.save()

        else:
            messages.error(request, 'Invalid credentials')

    
    return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'cart_total_price': cart_total_price, 'cart_quantity': cart_quantity, 'form': form, 'payment_form': payment_form})
    
