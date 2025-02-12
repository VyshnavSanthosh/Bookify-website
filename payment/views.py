from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingForm, PaymentForm
from store.models import Product
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
        if 'my_shipping' not in request.session:
            messages.error(request, 'Shipping details not found. Please fill out the shipping form.')
            return redirect('checkout')  # Redirect to the checkout page or wherever appropriate
        
        my_shipping = request.session['my_shipping']
        if request.user.is_authenticated:
            user = request.user
            fullname = my_shipping.get('shipping_fullname')
            email = my_shipping.get('shipping_email')
            shipping_address = f"{my_shipping.get('shipping_address1')}\n{my_shipping.get('shipping_address2')}\n {my_shipping.get('shipping_state')}\n {my_shipping.get('shipping_city')}\n {my_shipping.get('shipping_pincode')}"
            amount_paid = cart_total_price
            create_order = Order(user = user, fullname = fullname, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()
            
            #get the order id
            order_id = create_order.pk
            print(f"Cart Products: {cart_products}")
            print(f"Cart Quantity: {cart_quantity}")
            print(f"User authenticated: {request.user.is_authenticated}")
            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                for key, value in cart_quantity.items():
                    if int(key) == product_id:
                        print(f"Attempting to save OrderItem: order_id={order_id}, product_id={product_id}, user={user}, quantity={value}, price={product_price}")
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=product_price)
                        try:
                            create_order_item.save()
                            print(f"OrderItem saved successfully for product_id={product_id}.")
                        except Exception as e:
                            print(f"Error saving order item: {e}")
            messages.success(request, 'Order successfully placed.')
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del  request.session[key]
            return redirect('home')
    else:
        return redirect('home')

def shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = True)
        items = OrderItem.objects.filter(order__in = orders)
        return render(request, 'payment/shipped_dashboard.html', {'orders': orders, 'items': items})
    else:
        return render(request, 'payment/home.html',)

def unshipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped = False)
        items = OrderItem.objects.filter(order__in = orders)
        return render(request, 'payment/unshipped_dashboard.html', {'orders': orders, 'items': items})
    else:
        return render(request, 'payment/home.html',)

