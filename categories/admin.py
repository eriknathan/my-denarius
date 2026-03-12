from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category_type', 'created_at']
    list_filter = ['category_type']
    search_fields = ['name', 'user__email']
