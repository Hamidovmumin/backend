from cart.models import Cart,CartItem
from crud.cart import cart_crud,cart_item_crud
from serializers.cart import AddCartSerializer,ListCartItemSerializer,CartItemSerializer,CartResponseSerializer
from book.models import Book
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import uuid
from rest_framework import generics
from mptt.utils import get_cached_trees
from accounts.models import Users
from crud.book import book_crud
from utils.services import get_exchange_rate

@extend_schema(
    tags=["Cart"],
    responses={200: CartResponseSerializer,},
    summary="List all Cart",
)
# class CartListView(APIView):
#     def get(self, request):
#         cart_id = request.COOKIES.get("cart_id")
#         if not cart_id:
#             return Response([])
#         qs = CartItem.objects.filter(
#             cart__cart_id=cart_id
#         ).select_related("product")
#         data = ListCartItemSerializer().to_representation(qs)
#         return Response(data)
class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=self.request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        return CartItem.objects.filter(
            cart__cart_id=cart_id
        ).select_related("product").order_by("id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # sebətdəki unikal valyutalar üçün rate-ləri əvvəlcədən bir dəfə yüklə
        currencies = set(
            queryset.values_list("product__currency", flat=True)
        )
        rates = {
            currency: get_exchange_rate(from_currency=currency)
            for currency in currencies
        }

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={**self.get_serializer_context(), "rates": rates},
        )
        data = serializer.to_representation(queryset)

        return Response(data)


@extend_schema(
    tags=["Cart"],
    summary="Add to Cart",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
)
class AddToCartView(APIView):

    def post(self, request):
        new_cart = False
        product_id = request.query_params.get("product_id")

        product = get_object_or_404(
            Book,
            pk=product_id
        )

        if request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        if not cart_id:
            cart_id = str(uuid.uuid4())

            cart_crud.create(
                user=request.user if request.user.is_authenticated else None,
                cart_id=cart_id,
            )
            new_cart = True

        cart = cart_crud.get_cart_id(cart_id=cart_id)

        cart_item = cart_item_crud.get_cart_id(
            cart_id=cart_id,
            product_id=product.id,
        )

        if cart_item:
            return Response({
                "info": "Məhsul səbətə əlavə olunub!",
            })

        cart_item_crud.create(
            cart=cart,
            product=product,
            quantity=1,
        )

        response = Response({
            "successful": "Səbətə uğurla əlavə olundu",
        })

        if new_cart:
            response.set_cookie(
                "cart_id",
                cart_id,
                max_age=60 * 60 * 24 * 30,
                httponly=True,
                samesite="Lax"
            )

        return response




@extend_schema(
    tags=["Cart"],
    summary="Increment Cart Item Quantity",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
)
class IncrementCartItem(APIView):
    def post(self, request):
        product_id = request.query_params.get("product_id")

        if request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        cart_item = CartItem.objects.filter(
            cart__cart_id=cart_id,
            product_id=product_id,
        ).first()

        if not cart_item:
            return Response(
                {"error": "Məhsul səbətdə tapılmadı."},
                status=404,
            )

        product = book_crud.get_book_id(book_id=int(product_id))

        if cart_item.quantity >= 10:
            return Response({
                "info": "Məhsulun sayı 10 - dan çox ola bilməz!",
            })

        if product.stock > cart_item.quantity:
            cart_item.quantity +=1
            cart_item.save(update_fields=["quantity"])

            return Response({
                "successful": "Məhsulun sayı artırıldı.",
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity,
            })

        return Response({
            "info": "Məhsulun sayı stokdakı saydan cox ola bilməz!",
        })



@extend_schema(
    tags=["Cart"],
    summary="Decrement Cart Item Quantity",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
)
class DecrementCartItem(APIView):
    def post(self, request):
        product_id = request.query_params.get("product_id")
        if request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        cart_item = CartItem.objects.filter(
            cart__cart_id=cart_id,
            product_id=product_id,
        ).first()

        if not cart_item:
            return Response(
                {"error": "Məhsul səbətdə tapılmadı."},
                status=404,
            )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save(update_fields=["quantity"])

        return Response({
            "successful": "Məhsulun sayı azaldıldı.",
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
        })


@extend_schema(
    tags=["Cart"],
    summary="Delete Cart Item Quantity",
    parameters=[
        OpenApiParameter(
            name="product_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
)
class DeleteCartItem(APIView):

    def delete(self, request):
        product_id = request.query_params.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id tələb olunur."},
                status=400
            )

        if request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        if not cart_id:
            return Response(
                {"error": "Səbət tapılmadı."},
                status=404
            )

        cart_item = CartItem.objects.filter(
            cart__cart_id=cart_id,
            product_id=product_id,
        ).first()

        if not cart_item:
            return Response(
                {"error": "Məhsul səbətdə tapılmadı."},
                status=404
            )

        cart_item.delete()

        return Response({
            "successful": "Məhsul səbətdən silindi."
        })





