from django.db import transaction
from crud.cart import cart_crud
from cart.models import Cart,CartItem


@transaction.atomic
def merge_carts(user : Cart,guest_cart_id):
    user_cart = cart_crud.get_cart_user(user = user)
    guest_cart = cart_crud.get_cart_id(cart_id = guest_cart_id)

    guest_items = CartItem.objects.filter(cart=guest_cart)

    for guest_item in guest_items:

        user_item = CartItem.objects.filter(
            cart=user_cart,
            product=guest_item.product
        ).first()

        if user_item:
            # Eyni məhsul artıq user-in cartındadır
            user_item.quantity += guest_item.quantity
            user_item.save(update_fields=["quantity"])

            guest_item.delete()

        else:
            # Məhsul user-in cartında yoxdursa,
            # sadəcə cart-ını dəyiş
            guest_item.cart = user_cart
            guest_item.save(update_fields=["cart"])

    guest_cart.delete()


