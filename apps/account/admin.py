from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import AccountModel, TokenModel


@admin.register(AccountModel)
class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "is_email_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    # Add is_email_verified to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Info", {"fields": ("is_email_verified",)}),
    )


@admin.register(TokenModel)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("token", "user", "purpose", "expires_at")
    list_filter = ("purpose", "expires_at")
    search_fields = ("user__email", "user__username", "token")
    readonly_fields = ("expires_at",)
