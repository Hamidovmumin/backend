from django.db import models
from writer.models import Writer
from choices.role_choices import Role
from models.base import BaseDatabaseModel


class BookAuthor(BaseDatabaseModel):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE,related_name='book_authors')
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE,related_name='writer_books')
    role = models.CharField(choices=Role.choices,max_length=10)

    order = models.PositiveIntegerField(default=0)  # müəllif sırası

    is_primary = models.BooleanField(default=False)  # əsas müəllif

    class Meta:
        ordering = ['order']
        unique_together = ('book', 'writer')

    def __str__(self):
        return f"{self.book} - {self.writer} ({self.role})"
