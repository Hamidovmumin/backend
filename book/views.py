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
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from mptt.utils import get_cached_trees
from serializers.category import CategoryTreeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from book.filters import BookFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter

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

    queryset = Book.objects.all().order_by('-id').select_related('category').prefetch_related(
        Prefetch(
            'book_authors',
            queryset=BookAuthor.objects.filter(is_primary=True).select_related('writer'),
            to_attr='primary_authors_list'
        )
    )
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BookCursorPagination


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
            description='Category name (e.g. Fiction)'
        )
    ]
)
class GetCategoryBookAll(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-id').select_related('category').prefetch_related(
        Prefetch(
            'book_authors',
            queryset=BookAuthor.objects.filter(is_primary=True).select_related('writer'),
            to_attr='primary_authors_list'
        )
    )
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter