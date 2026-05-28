from django.contrib import admin
from book.models import Book
from author.models import BookAuthor
from book.form import BookAdminForm


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm

    list_display = (
        "book_name",
        "category",
        "price",
        "discount",
        "stock",
        "currency",
        "rating_average",
        "is_active",
    )

    list_filter = (
        "category",
        "currency",
        "is_active",
        "published_at",
    )

    search_fields = (
        "book_name",
        "isbn",
        "description",
    )

    prepopulated_fields = {"slug": ("book_name",)}

    filter_horizontal = (
        "tag",
    )

    readonly_fields = (
        "views",
        "rating_average",
        "rating_count",
    )

    inlines = [BookAuthorInline]

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "book_name",
                "slug",
                "description",
                "image",
                "category",
                "tag",
            )
        }),
        ("Details", {
            "fields": (
                "page_size",
                "language",
                "isbn",
                "published_at",
            )
        }),
        ("Pricing & Stock", {
            "fields": (
                "price",
                "discount",
                "currency",
                "stock",
            )
        }),
        ("Stats", {
            "fields": (
                "views",
                "rating_average",
                "rating_count",
            )
        }),
        ("SEO", {
            "fields": (
                "meta_title",
                "meta_description",
            )
        }),
        ("Status", {
            "fields": (
                "is_active",
            )
        }),
    )