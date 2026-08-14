from crud.auth.base import CRUDSession
from cart.models import Cart,CartItem
from typing import Optional
from book.models import Book
from accounts.models import Users


class CRUDBook(CRUDSession[Book]):

    def get_book_id(self,book_id:int)->Optional[Book]:
        try:
            return Book.objects.get(id=book_id)
        except self.model.DoesNotExist:
            return None

book_crud = CRUDBook(Book)