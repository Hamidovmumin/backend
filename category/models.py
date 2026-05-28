from django.db import models
from models.base import BaseDatabaseModel
from mptt.models import MPTTModel, TreeForeignKey

class Category(BaseDatabaseModel,MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category/', blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    def __str__(self):
        return self.name

# class Category(BaseDatabaseModel):
#     name = models.CharField(max_length=100,unique=True)
#     slug = models.SlugField(max_length=100,unique=True)
#     description = models.TextField(blank=True)
#     image = models.ImageField(upload_to='category/',blank=True)
#     parent = models.ForeignKey(
#         'self',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='children',
#     )
#     is_active = models.BooleanField(default=False)
#     order = models.PositiveIntegerField(default=0)
#
#     class Meta:
#         ordering = ['order','name']
#         verbose_name = 'Categories'
#         verbose_name_plural = 'Categories'
#
#     def __str__(self):
#         return self.name


