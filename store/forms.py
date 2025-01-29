from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

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

