from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from author.models import BookAuthor
from book.models import Book
from category.models import Category
from serializers.book import BookListSerializer
from rest_framework.throttling import AnonRateThrottle
from utils.pagination import BookCursorPagination
from django.db.models import Prefetch
from mptt.utils import get_cached_trees
from serializers.category import CategoryTreeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from book.filters import BookFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from cart.models import Cart,CartItem
from django.db.models import Exists, OuterRef
from crud.cart import cart_crud

@extend_schema(
    tags=["Books"],
    responses={200: BookListSerializer,},
    summary="List all books",
)
class BookList(generics.ListAPIView):
    # queryset = Book.objects.all().order_by('-id').prefetch_related(
    #     Prefetch(
    #         'book_authors',
    #         queryset=BookAuthor.objects.filter(is_primary=True).select_related('writer'),
    #     )
    # )

    # queryset = Book.objects.all().order_by('-id').select_related('category').prefetch_related(
    #     Prefetch(
    #         'book_authors',
    #         queryset=BookAuthor.objects.filter(is_primary=True).select_related('writer'),
    #         to_attr='primary_authors_list'
    #     )
    # )


    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BookCursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get_queryset(self):
        if self.request.user.is_authenticated and (cart := cart_crud.get_cart_user(user=self.request.user)):
            cart_id = cart.cart_id
        else:
            cart_id = self.request.COOKIES.get("cart_id")

        queryset = (
            Book.objects
            .all()
            .order_by("-id")
            .select_related("category")
            .prefetch_related(
                Prefetch(
                    "book_authors",
                    queryset=BookAuthor.objects.filter(
                        is_primary=True
                    ).select_related("writer"),
                    to_attr="primary_authors_list",
                )
            )
        )

        # if not cart_id:
        #     return queryset.annotate(
        #         cart=False
        #     )

        cart_items = CartItem.objects.filter(
            cart__cart_id=cart_id,
            product=OuterRef("pk"),
        )

        return queryset.annotate(
            cart=Exists(cart_items)
        )


@extend_schema(
    tags=["Books"],
    responses={200: CategoryTreeSerializer,},
    summary="List all category books",
)
class CategoryTreeView(APIView):
    def get(self, request):
        qs = Category.objects.filter(is_active=True)
        roots = get_cached_trees(qs)
        data = CategoryTreeSerializer().to_representation(roots)
        return Response(data)



@extend_schema(
    tags=["Books"],
    responses={200: BookListSerializer},
    summary="List all books by Category",
    parameters=[
        OpenApiParameter(
            name='category',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Category slug (e.g. klassik-roman)'
        ),
        OpenApiParameter(
            name='min_price',
            type=float,
            location=OpenApiParameter.QUERY,
            description='Minimum price'
        ),
        OpenApiParameter(
            name='max_price',
            type=float,
            location=OpenApiParameter.QUERY,
            description='Maximum price'
        ),
    ]
)
class GetCategoryBooks(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-id').select_related('category').prefetch_related(
        Prefetch(
            'book_authors',
            queryset=BookAuthor.objects.filter(is_primary=True).select_related('writer'),
            to_attr='primary_authors_list'
        )
    )
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = BookCursorPagination
    filterset_class = BookFilter


class AddCart(APIView):
    def post(self, request):
        pass