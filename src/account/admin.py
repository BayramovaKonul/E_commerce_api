from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUserModel, UserProfileModel, ForgotPasswordTokenModel, ValidateUserTokenModel

@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    search_fields = ("email","first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "password1", "password2", "is_staff",
                "is_active", "is_superuser",
            )}
        ),
    )

@admin.register(ForgotPasswordTokenModel)
class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ['user__email','token', 'is_used']
    search_fields = ['user__email', 'is_used'] 
    list_filter = ['is_used', 'expired_at']


@admin.register(ValidateUserTokenModel)
class ValidateUserAdmin(admin.ModelAdmin):
    list_display = ['user__email','token', 'is_used']
    search_fields = ['user__email', 'is_used'] 
    list_filter = ['is_used', 'expired_at']


@admin.register(UserProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__email','birthday', 'phone_number']
    search_fields = ['user__email', 'birthday'] 
    list_filter = ['birthday']