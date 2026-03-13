from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from transactions.models import Transaction
from .forms import BudgetForm
from .models import Budget


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budgets/list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return (
            Budget.objects
            .filter(user=self.request.user)
            .select_related('category')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()

        spending = {}
        rows = (
            Transaction.objects
            .filter(
                user=user,
                transaction_type='expense',
                date__month=today.month,
                date__year=today.year,
                category__isnull=False,
            )
            .values('category_id')
            .annotate(total=Sum('amount'))
        )
        for row in rows:
            spending[row['category_id']] = row['total']

        enriched = []
        for budget in context['budgets']:
            spent = spending.get(budget.category_id, Decimal('0'))
            percentage = min(int(spent / budget.amount * 100), 100) if budget.amount else 0
            over_amount = max(spent - budget.amount, Decimal('0'))
            enriched.append({
                'budget': budget,
                'spent': spent,
                'remaining': max(budget.amount - spent, Decimal('0')),
                'percentage': percentage,
                'over_budget': spent > budget.amount,
                'over_amount': over_amount,
            })
        context['enriched'] = enriched
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/form.html'
    success_url = reverse_lazy('budgets:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Meta de orçamento criada com sucesso.')
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/form.html'
    success_url = reverse_lazy('budgets:list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Meta atualizada com sucesso.')
        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budgets/confirm_delete.html'
    success_url = reverse_lazy('budgets:list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Meta excluída com sucesso.')
        return super().form_valid(form)
