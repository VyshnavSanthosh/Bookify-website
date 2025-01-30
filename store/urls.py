
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('login/', views.login_user , name='login'),
    path('logout/', views.logout_user , name='logout'),
    path('register/', views.register_user , name = 'registration'),
    path('product_detail/<int:pk>', views.product_detail , name='product_detail'),
    path('category/<str:ctry>', views.category , name='category'),
    path('update_user/', views.update_user , name='update_user'),
    path('update_profile/', views.update_profile , name='update_profile'),
    path('update_password/', views.update_password , name='update_password'),
]
