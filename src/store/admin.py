from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import StoreModel


@admin.register(StoreModel)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','owner', 'description']
    search_fields = ['name', 'owner'] 
    list_filter = ['created_at']