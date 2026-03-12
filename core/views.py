import json
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

        # Saldo real: soma current_balance de todas as contas
        accounts = Account.objects.filter(user=user)
        current_balance = sum(
            a.current_balance for a in accounts
        )

        total_income = (
            Transaction.objects.filter(
                user=user,
                transaction_type='income',
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )

        total_expenses = (
            Transaction.objects.filter(
                user=user,
                transaction_type='expense',
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )

        net_month = total_income - total_expenses

        recent_transactions = (
            Transaction.objects.filter(user=user)
            .select_related('account', 'category')[:5]
        )

        # --- Dados para gráficos ---

        # Pizza: despesas por categoria no mês
        category_breakdown = list(
            Transaction.objects.filter(
                user=user,
                transaction_type='expense',
                date__month=today.month,
                date__year=today.year,
                category__isnull=False,
            )
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        cat_labels = [c['category__name'] for c in category_breakdown]
        cat_values = [float(c['total']) for c in category_breakdown]

        # Barras: receitas vs despesas dos últimos 6 meses
        month_labels = []
        month_incomes = []
        month_expenses_list = []
        month_names = [
            'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',
        ]
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            month_labels.append(f'{month_names[m - 1]}/{y}')
            inc = (
                Transaction.objects.filter(
                    user=user,
                    transaction_type='income',
                    date__month=m,
                    date__year=y,
                ).aggregate(t=Sum('amount'))['t']
                or Decimal('0')
            )
            exp = (
                Transaction.objects.filter(
                    user=user,
                    transaction_type='expense',
                    date__month=m,
                    date__year=y,
                ).aggregate(t=Sum('amount'))['t']
                or Decimal('0')
            )
            month_incomes.append(float(inc))
            month_expenses_list.append(float(exp))

        context['current_balance'] = current_balance
        context['total_income'] = total_income
        context['total_expenses'] = total_expenses
        context['net_month'] = net_month
        context['recent_transactions'] = recent_transactions

        # Chart data como JSON seguro para JS
        context['chart_cat_labels'] = json.dumps(
            cat_labels, ensure_ascii=False,
        )
        context['chart_cat_values'] = json.dumps(cat_values)
        context['chart_month_labels'] = json.dumps(
            month_labels, ensure_ascii=False,
        )
        context['chart_month_incomes'] = json.dumps(
            month_incomes,
        )
        context['chart_month_expenses'] = json.dumps(
            month_expenses_list,
        )
        return context


