from django.contrib import admin
from .models import WishlistModel, CartModel

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