from rest_framework.pagination import CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 8
    max_page_size = 100
    ordering = ('-id',)
    cursor_query_param = 'cursor'