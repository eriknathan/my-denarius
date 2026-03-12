from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'transaction_type', 'amount', 'date', 'account', 'category']
    list_filter = ['transaction_type', 'date', 'account', 'category']
