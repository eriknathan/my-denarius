from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('checking', 'Corrente'),
        ('savings', 'Poupança'),
        ('cash', 'Dinheiro'),
        ('other', 'Outro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
    )
    initial_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def current_balance(self):
        """Saldo real: inicial + receitas - despesas."""
        income = (
            self.transactions
            .filter(transaction_type='income')
            .aggregate(total=Sum('amount'))['total']
        ) or Decimal('0')
        expenses = (
            self.transactions
            .filter(transaction_type='expense')
            .aggregate(total=Sum('amount'))['total']
        ) or Decimal('0')
        return self.initial_balance + income - expenses
