from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('menu', views.menu, name='menu'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('cart', views.cart, name='cart'),
    path('remove_item', views.remove_item, name='remove_item'),
    path('cart_partial', views.cart, name='cart_partial'),
    path('checkout', views.checkout, name='checkout'),
]