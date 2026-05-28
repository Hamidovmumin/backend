from django.contrib import admin
from writer.models import Writer


@admin.register(Writer)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['writer', 'slug', 'description', ]
    list_filter = ('writer','created_at')
    search_fields = ('writer','slug')
    prepopulated_fields = {
        'slug': ('writer',)
    }

    ordering = ( 'writer',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Full name writer', {
            'fields': ('writer', 'slug',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )

