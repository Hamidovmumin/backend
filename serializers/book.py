from rest_framework import serializers
from book.models import Book
from writer.models import Writer
from django.db.models import Prefetch

class BookListSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    category = serializers.ReadOnlyField(source='category.name')
    cart = serializers.BooleanField(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'image','category','price','currency','writer','cart','rating_average']

    def get_writer(self, obj):
        authors = obj.primary_authors_list
        if authors:
            return authors[0].writer.writer
        return None
