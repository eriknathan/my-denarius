from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'account', 'category', 'amount', 'transaction_type', 'date']
    list_filter = ['transaction_type', 'date', 'account']
    search_fields = ['description', 'user__email']
