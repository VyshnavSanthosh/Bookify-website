from django.shortcuts import render, redirect
from .models import Category, Customer, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm,UserProfileUpdateForm,UpdatePasswordForm
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    products = Product.objects.all().order_by('name')  # Order by name 
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'home.html', {'products': products})




def category(request, ctry):
    ctry = ctry.replace('-', ' ')
    try:
        category_items = Category.objects.get(name=ctry)
        product_category = Product.objects.filter(category=category_items)
        paginator = Paginator(product_category, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'catergory.html', {'product_category': product_category, 'category_items': category_items, 'page_obj': page_obj})
    except Category.DoesNotExist:
        messages.error(request, f"Category '{ctry}' doesn't exist")
        return redirect('home')


def product_detail(request, pk):
    product_detail = Product.objects.get(id=pk)
    return render(request, 'product_detail.html' , {'product_detail':product_detail})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username , password=password )
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html' , {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_form = UserProfileUpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User has been updated successfully.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form, 'current_user': current_user})
    else:
        return redirect('login')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method =='POST':
            form = UpdatePasswordForm(current_user , request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password has been updated successfully.')
                return redirect('home')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
        return render(request, 'update_password.html', {'form': form, 'current_user': current_user})
    else:
        return redirect('login')

def register_user(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(request, username=username 	, password=password)
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})