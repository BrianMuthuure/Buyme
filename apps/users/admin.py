from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    readonly_fields = ["date_joined", "last_login"]
    list_display = [
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "birth_date",
        "age",
        "is_active",
        "is_superuser",
        "is_staff",
    ]

    list_filter = ["is_superuser", "is_staff", "is_active"]

    fieldsets = (
        ("Login Credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "middle_name", "last_name", "birth_date")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
        ("Important dates", {"fields": ("date_joined", "last_login",)}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
