from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','password1','password2') 
        
class UserProfileUpdateForm(UserChangeForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class UserInfoUpdateForm(forms.ModelForm):
    phone = forms.CharField(required=False)  # Set required to False
    address1 = forms.CharField(required=False)  # Set required to False
    address2 = forms.CharField(required=False)  # Set required to False
    state = forms.CharField(required=False)  # Set required to False
    city = forms.CharField(required=False)  # Set required to False
    pincode = forms.CharField(required=False)  # Set required to False

    class Meta:
        model = Profile
        fields = ['phone','address1', 'address2', 'state', 'city', 'pincode']

class ProductSearch(forms.Form):
    query = forms.CharField(label='Search Products', max_length=100, required=False)