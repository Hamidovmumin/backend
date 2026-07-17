import django_filters
from book.models import Book

class BookFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )

    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )

    class Meta:
        model = Book
        fields = ['category', 'min_price', 'max_price']