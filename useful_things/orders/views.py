from django.shortcuts import render, redirect
from .models import Product, CartContainer
from django.shortcuts import get_object_or_404
from banners.models import Banner


def index(request):
    template = 'orders/index.html'
    products = Product.objects.all()[:12]
    banners = Banner.objects.filter(is_active=True)
    context = {
        'products': products,
        'banners': banners
    }
    return render(request, template, context)


def product_detail(request, pk):
    template = 'orders/product-detail.html'
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.cycle_key()
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, template, context)


def cart(request):
    template = 'orders/cart.html'
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.cycle_key()
    cart_containers = CartContainer.objects.filter(session_key=session_key)
    cart_container_count = len(cart_containers)
    context = {
        'cart_containers': cart_containers,
        'cart_container_count': cart_container_count
    }
    return render(request, template, context)


def add_to_cart(request, pk):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.cycle_key()
    product = get_object_or_404(Product, pk=pk)
    CartContainer.objects.create(
        product=product,
        session_key=session_key
    )
    return redirect('orders:cart')


def delete_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.cycle_key()
    cart_container = get_object_or_404(
        CartContainer,
        product=product,
        session_key=session_key
    )
    cart_container.delete()
    return redirect('orders:cart')
