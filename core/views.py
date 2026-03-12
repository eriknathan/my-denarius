from decimal import Decimal

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'public/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()

        Account = apps.get_model('accounts', 'Account')
        Transaction = apps.get_model('transactions', 'Transaction')

        total_balance = Account.objects.filter(user=user).aggregate(
            total=Sum('initial_balance')
        )['total'] or Decimal('0.00')

        total_income = Transaction.objects.filter(
            user=user,
            transaction_type='income',
            date__month=today.month,
            date__year=today.year,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        total_expenses = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            date__month=today.month,
            date__year=today.year,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        recent_transactions = Transaction.objects.filter(
            user=user,
        ).select_related('account', 'category')[:5]

        context['total_balance'] = total_balance
        context['total_income'] = total_income
        context['total_expenses'] = total_expenses
        context['recent_transactions'] = recent_transactions
        return context
