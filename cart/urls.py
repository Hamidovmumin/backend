from django.urls import path
from cart.views import AddToCartView, CartListView,IncrementCartItem,DecrementCartItem,DeleteCartItem

urlpatterns = [
    path("cart-list/", CartListView.as_view(), name="cart-list"),
    path("cart-add/", AddToCartView.as_view(), name="add-to-cart"),
    path('cart-increment/', IncrementCartItem.as_view(), name='cart-increment'),
    path('cart-decrement/', DecrementCartItem.as_view(), name='cart-decrement'),
    path('cart-delete/', DeleteCartItem.as_view(), name='cart-delete'),
]