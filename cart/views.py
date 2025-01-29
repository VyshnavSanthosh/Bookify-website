from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, response

# Create your views here.



def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    cart_quantity = cart.__len__()
    product_quantity = cart.get_total_quantity()
    total_price = cart.get_total_price()  # Get total price of items in the cart
    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'cart_quantity': cart_quantity,
        'product_quantity': product_quantity,
        'total_price': total_price,  # Pass total price to template
    })

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        product = get_object_or_404(Product, id=int(product_id))
        cart.add(product=product, product_quantity=int(product_quantity))
        cart_quantity = cart.__len__()
        messages.success(request, f"{product.name} has been added to the cart")
        return JsonResponse({'count': f'{cart_quantity}'})

    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=int(product_id))
        cart.remove(product_id)
        response = JsonResponse({'product_id': product_id})
        messages.success(request, f"{product.name} has been removed from the cart")
        return response



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        product = get_object_or_404(Product, id=int(product_id))
        messages.success(request, f"{product.name} quantity has been updated")
        cart.update(product_id = product_id , product_quantity = product_quantity)
        response = JsonResponse({'qty': product_quantity})

        return response


