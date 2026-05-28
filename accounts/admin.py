from django.contrib import admin
from accounts.models import Users
from django.contrib.auth.admin import UserAdmin

@admin.register(Users)
class UsersAdmin(UserAdmin):

    list_display = ['email', 'first_name', 'last_name', 'username', 'is_active', 'is_superuser', 'is_staff']
    list_display_links = ['email', 'first_name', 'last_name', ]
    list_filter = ("email","is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username", "phone_number")
    readonly_fields = ('last_login', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        ("Login Info", {
            "fields": ("email", "password")
        }),

        ("Personal Info", {
            "fields": ("username", "first_name", "last_name", "phone_number")
        }),

        ("Security - Password", {
            "fields": (
                "password_changed",
                "bad_password_time",
                "bad_password_count",
                "block_time",
            )
        }),

        ("Security - Email Verification", {
            "fields": (
                "email_is_confirmed",
                "email_code_limit",
                "bad_email_code_time",
                "bad_email_code_count",
            )
        }),

        ("Security - TOTP (2FA)", {
            "fields": (
                "totp_token",
                "totp_is_confirmed",
                "bad_totp_code_time",
                "bad_totp_code_count",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_admin",
                "is_staff",
                "is_active",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": ("last_login",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "phone_number", "password1", "password2",
                       "is_staff", "is_active", "is_superuser", "groups", "user_permissions"),
        }),
    )


