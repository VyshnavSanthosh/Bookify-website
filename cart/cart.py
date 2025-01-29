from store.models import Product
from decimal import Decimal

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # get the current session key if it exist
        
        cart = self.session.get('session_key')
        
        # if the session is not exist create a new one
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # make sure cart is available to all pages of site
        self.cart = cart
        
    def add(self, product, product_quantity):
        product_id = str(product.id)
        product_quantity = str(product_quantity)
        if product_id in self.cart:
            # quantity = int(self.cart[product]['quantity'] + 1)
            pass
        
        else:
            self.cart[product_id] = int(product_quantity)
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(pk__in = product_id)
        return products
    
    def get_total_quantity(self):
        quantity = self.cart
        return quantity
    
    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = str(product_quantity)
        
        ourcart = self.cart
        ## update the quantity of the item in cart(dictionary)
        ourcart[product_id] = product_quantity
        self.session.modified = True
        updt = self.cart
        return updt

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
    def get_total_price(self):
        total_price = Decimal(0)  # Initialize total_price as a Decimal
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(id=int(product_id))  # Fetch product by ID
            if product.is_sale:
                total_price += product.sale_price * Decimal(quantity)
            else:
                total_price += product.price * Decimal(quantity)  # Convert quantity to Decimal
        return total_price

