from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUserModel

@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    search_fields = ("email","fullname")
    ordering = ("email",)
    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("fullname",)}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "fullname", "password1", "password2", "is_staff",
                "is_active", "is_superuser",
            )}
        ),
    )
