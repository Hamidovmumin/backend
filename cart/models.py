from __future__ import annotations
import uuid
from django.db import models
from models.base import BaseDatabaseModel
from accounts.models import Users
from book.models import Book

class Cart(BaseDatabaseModel):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        null=True,blank=True,
        related_name='carts'
    )
    cart_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    def __str__(self):
        return str(self.cart_id)

class CartItem(BaseDatabaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_cart_product'
            )
        ]

    def __str__(self):
        return f'{self.product}'
