from rest_framework import serializers
from cart.models import CartItem
from utils.services import get_exchange_rate
from decimal import Decimal, ROUND_HALF_UP


class AddCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)


class ListCartItemSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        items = super().to_representation(data)

        cart_total = sum(
            item["item_total"]
            for item in items
        )

        return {
            "items": items,
            "cart_total": cart_total,
        }


class CartItemSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )
    name = serializers.CharField(
        source="product.book_name",
        read_only=True
    )
    image = serializers.ImageField(
        source="product.image",
        read_only=True
    )
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    currency = serializers.CharField(
        source="product.currency",
        read_only=True
    )
    stock = serializers.IntegerField(
        source="product.stock",
        read_only=True
    )
    price_to_azn = serializers.SerializerMethodField()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "name",
            "image",
            "price",
            "currency",
            "stock",
            "price_to_azn",
            "quantity",
            "item_total",
        ]
        list_serializer_class = ListCartItemSerializer

    def get_price_to_azn(self, obj):
        # context-dən əvvəlcədən yüklənmiş rate-lər gəlirsə, Redis-ə getmə
        rates = self.context.get("rates")
        currency = obj.product.currency

        if rates is not None and currency in rates:
            rate = rates[currency]
        else:
            rate = get_exchange_rate(from_currency=currency)

        price = Decimal(str(obj.product.price))
        total = price * rate
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_item_total(self, obj):
        return obj.quantity * self.get_price_to_azn(obj)


class CartResponseSerializer(serializers.Serializer):
    """
    YALNIZ Swagger/schema üçündür (drf-spectacular).
    Real serializasiya prosesində istifadə OLUNMUR.
    """
    items = CartItemSerializer(many=True)
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)




# class ListCartItemSerializer(serializers.Serializer):
    # def to_representation(self, instance):
    #
    #     items = [self.product_detail(item) for item in instance]
    #     cart_total = sum(
    #         item['item_total']
    #         for item in items
    #     )
    #     return {
    #         "items": items,
    #         "cart_total": cart_total,
    #     }
    #
    # @staticmethod
    # def product_detail(item):
    #     return {
    #         "id": item.product_id,
    #         "name": item.product.book_name,
    #         "image": item.product.image.url,
    #         "price": item.product.price,
    #         "quantity": item.quantity,
    #         "item_total": item.quantity * item.product.price,
    #     }


