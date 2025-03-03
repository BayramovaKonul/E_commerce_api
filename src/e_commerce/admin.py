from django.contrib import admin
from .models import WishlistModel

@admin.register(WishlistModel)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'product__name', 'updated_at']
    list_display_links = ['user__email', 'product__name', 'updated_at'] 
    search_fields = ['user__email'] 
    list_filter = ['created_at']