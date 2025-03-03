from django.contrib import admin

from django.contrib import admin
from .models import ProductModel, CategoryModel, ProductImageModel, CommentModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'price']
    list_display_links = ['name', 'store'] 
    search_fields = ['name', 'store', 'categories'] 
    list_filter = ['created_at', 'price', 'stock']


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_display_links = ['name',] 
    search_fields = ['name', ] 
    list_filter = ['created_at',]


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product__name']
    list_display_links = ['product__name'] 
    search_fields = ['product__name'] 
    list_filter = ['created_at']


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'product__name', 'user__email', 'rating']
    list_display_links = ['comment', 'product__name', 'rating'] 
    list_filter = ['product__name', 'user__email', 'created_at', 'rating']