from django.contrib import admin
from django.urls import path, include
from .views import index, product_detail, cart, add_to_cart, delete_from_cart

app_name = 'orders'

urlpatterns = [
    path('', index, name='index'),
    path('product/<pk>', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('cart/add_to_cart/<pk>,', add_to_cart, name='add_to_cart'),
    path('cart/delete_from_cart/<pk>,', delete_from_cart, name='delete_from_cart')
]
