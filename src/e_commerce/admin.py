from django.contrib import admin
from .models import WishlistModel, CartModel, OrderDetailsModel, OrderModel

@admin.register(WishlistModel)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'product__name', 'updated_at']
    list_display_links = ['user__email', 'product__name', 'updated_at'] 
    search_fields = ['user__email'] 
    list_filter = ['created_at']


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user__email','product__name', 'quantity', 'product__price']
    list_display_links = ['user__email','product__name', 'quantity'] 
    search_fields = ['product__name', 'product__name'] 
    list_filter = ['quantity']


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'shipping_address', 'created_at']
    list_display_links = ['user__email', 'shipping_address'] 
    search_fields = ['shipping_address', 'user__email'] 
    list_filter = ['created_at',  'shipping_address']

@admin.register(OrderDetailsModel)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['product__name', 'cost', 'quantity', 'status']
    list_display_links = ['cost', 'quantity','status'] 
    search_fields = ['product__name', 'order__shipping_address', 'status'] 
    list_filter = ['cost', 'order__shipping_address', 'status']