from django.db import models
from category.models import Category
from models.base import BaseDatabaseModel
from choices.book_choices import Currency
from decimal import Decimal

class Book(BaseDatabaseModel):
    book_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='books/')
    description = models.TextField()
    page_size = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50,null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    writer = models.ManyToManyField('writer.Writer', through='author.BookAuthor', related_name='books')
    tag = models.ManyToManyField('tags.Tag', blank=True, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    currency = models.CharField(max_length=3,choices=Currency.choices, default='AZN')

    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    published_at = models.DateField(null=True, blank=True)

    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("0.00"))
    rating_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)


    def __str__(self):
        return self.book_name


