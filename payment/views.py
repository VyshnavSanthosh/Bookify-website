from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
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
            my_shipping = request.POST
            request.session['my_shipping'] = my_shipping

        else:
            messages.error(request, 'Invalid credentials')

    
    return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'cart_total_price': cart_total_price, 'cart_quantity': cart_quantity, 'form': form, 'payment_form': payment_form})
    
def process_order(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    cart_total_price = cart.get_total_price()
    cart_quantity = cart.get_total_quantity()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)  # Create a new form if no address exists
        my_shipping = request.session['my_shipping']
        if request.user.is_authenticated:
            user = request.user
            fullname = my_shipping.get('shipping_fullname')
            email = my_shipping.get('shipping_email')
            shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get('shipping_address2')}\n {my_shipping.get('shipping_state')}\n {my_shipping.get('shipping_city')}\n {my_shipping.get('shipping_pincode')}"
            amount_paid = cart_total_price
            create_order = Order(user = user, fullname = fullname, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()
            messages.success(request, 'Order successfully placed.')
            return redirect('payment_success')
    else:
        return redirect('home')

