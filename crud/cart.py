from crud.auth.base import CRUDSession
from cart.models import Cart,CartItem
from typing import Optional
from book.models import Book
from accounts.models import Users


class CRUDCart(CRUDSession[Cart]):

    def get_cart_id(self,cart_id:str)->Optional[Cart]:
        try:
            return Cart.objects.get(cart_id=cart_id)
        except self.model.DoesNotExist:
            return None

    def get_cart_user(self,user:Users)->Optional[Cart]:
        try:
            return Cart.objects.get(user=user)
        except self.model.DoesNotExist:
            return None

cart_crud = CRUDCart(Cart)


class CRUDCartItem(CRUDSession[CartItem]):

    def get_cart_id(self,cart_id:str,product_id:int)->Optional[CartItem]:
        try:
            return CartItem.objects.get(
                cart__cart_id=cart_id,
                product_id=product_id
            )
        except self.model.DoesNotExist:
            return None

cart_item_crud = CRUDCartItem(CartItem)