from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "cart_id",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "cart_id",
        "user__username",
        "user__email",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "cart_id",
        "created_at",
        "updated_at",
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "cart__cart_id",
        "product__name",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )