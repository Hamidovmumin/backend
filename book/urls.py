from django.urls import path
from book.views import BookList,CategoryTreeView,GetCategoryBooks

urlpatterns = [
    path('all/',BookList.as_view(),name='all-books'),
    path('all-category/',CategoryTreeView().as_view(),name='all-category'),
    path('get-books-category/',GetCategoryBooks.as_view(),name='category-books-all'),
]