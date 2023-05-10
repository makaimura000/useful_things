from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Container, Order, Product, CartContainer


class ContainerInline(admin.TabularInline):
    model = Container
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'value', 'category', 'old_value', 'discount', 'image_tag')
    list_editable = ('category',)
    readonly_fields = ('discount',)

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 80px" />'.format(obj.image.url))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description')
    readonly_fields = ('slug',)
    inlines = [ProductInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'updated', 'customer', 'value')
    readonly_fields = ('value',)
    inlines = [ContainerInline]


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'product', 'quantity', 'current_product_value', 'total_value')
    readonly_fields = ('current_product_value', 'total_value')


@admin.register(CartContainer)
class CartContainerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session_key', 'product', 'quantity', 'user', 'created')
