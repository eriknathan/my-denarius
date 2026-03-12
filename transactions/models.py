from django.conf import settings
from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='conta',
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='categoria',
    )
    description = models.CharField(max_length=200, verbose_name='descrição')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='valor',
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='tipo',
    )
    date = models.DateField(verbose_name='data')
    notes = models.TextField(blank=True, verbose_name='observações')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'transação'
        verbose_name_plural = 'transações'

    def __str__(self):
        return f'{self.description} - R$ {self.amount}'
