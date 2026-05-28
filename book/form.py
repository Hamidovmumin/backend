from django import forms
from mptt.forms import TreeNodeChoiceField
from category.models import Category
from book.models import Book

class BookAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        level_indicator='—'
    )

    class Meta:
        model = Book
        fields = '__all__'