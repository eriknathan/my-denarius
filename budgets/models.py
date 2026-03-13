from django.conf import settings
from django.db import models


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets',
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='budgets',
        verbose_name='categoria',
        limit_choices_to={'category_type': 'expense'},
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='valor limite',
    )
    month = models.DateField(
        verbose_name='mês de referência',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-month', 'category__name']
        verbose_name = 'meta de orçamento'
        verbose_name_plural = 'metas de orçamento'
        unique_together = [['user', 'category', 'month']]

    def __str__(self):
        return f'{self.category.name} — {self.month:%m/%Y} — R$ {self.amount}'
