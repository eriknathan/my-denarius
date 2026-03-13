---
name: budgets app architecture
description: Budget model, form, views, URLs, admin, and migration details for the budgets app (Metas de Orçamento)
type: project
---

The `budgets` app was created to support spending budget goals per expense category per month.

**Model:** `Budget` — ForeignKey to `AUTH_USER_MODEL` and `categories.Category` (limited to `category_type='expense'`). Fields: `amount` (DecimalField 12,2), `month` (DateField, stored as first day of month). `unique_together = [['user', 'category', 'month']]`. Ordering: `['-month', 'category__name']`.

**Form:** `BudgetForm` — receives `user` kwarg in `__init__` to filter category queryset to `expense` only. `clean_month()` handles the HTML `<input type="month">` format (`YYYY-MM`) converting it to `datetime.date(year, month, 1)`. Has dark mode aware `INPUT_CLASS`.

**Views:** Standard CBV pattern — `BudgetListView`, `BudgetCreateView`, `BudgetUpdateView`, `BudgetDeleteView`. `BudgetListView.get_context_data()` enriches each budget with current-month spending (via `Transaction.objects.filter(...).values('category_id').annotate(total=Sum('amount'))`), computing `spent`, `remaining`, `percentage`, `over_budget`, `over_amount`.

**URLs:** `app_name = 'budgets'`, mounted at `orcamento/` in `core/urls.py`. Route names: `list`, `create`, `update`, `delete`. Portuguese path segments: `nova/`, `<pk>/editar/`, `<pk>/excluir/`.

**Admin:** `BudgetAdmin` with `list_display`, `list_filter = ['month']`, `raw_id_fields = ['user']`.

**Migration:** `budgets/migrations/0001_initial.py` — applied cleanly.

**Why:** To allow users to set monthly spending limits per expense category and track whether they are over budget.

**How to apply:** When adding features to budgets, note the `clean_month` pattern is needed because `<input type="month">` submits `YYYY-MM` which Django's DateField cannot parse natively. Always filter Budget querysets by `request.user`.
