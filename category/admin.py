from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from category.models import Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):

    list_display = ('name','tree_actions', 'indented_title', 'parent','is_active', 'order')
    list_display_links = ('name',)

    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')

    prepopulated_fields = {
        'slug': ('name',)
    }

    list_editable = ('is_active', 'order')

    readonly_fields = ('created_at', 'updated_at')  # 🔥 əlavə et

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Content', {
            'fields': ('description', 'image')
        }),
        ('Status', {
            'fields': ('is_active', 'order')
        }),
    )