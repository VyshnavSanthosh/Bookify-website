from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_fullname = forms.CharField(required=False)
    shipping_email = forms.CharField(required=False)
    shipping_address1 = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_pincode = forms.CharField(required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_fullname', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_state', 'shipping_city', 'shipping_pincode']
        
        exclude = ['user',]
        
class PaymentForm(forms.Form):
    payment_fullname = forms.CharField(required=False)
    payment_cardnumber = forms.CharField(required=False)
    payment_cvv = forms.CharField(required=False)
    payment_expiry = forms.CharField(required=False)
    