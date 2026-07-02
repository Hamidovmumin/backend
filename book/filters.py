import django_filters
from book.models import Book

class BookFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    class Meta:
        model = Book
        fields = ['category']