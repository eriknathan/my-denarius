---
name: accounts app architecture
description: Account model, form, views, URLs, admin, and templates for the accounts app
type: project
---

Account model has fields: user (FK to AUTH_USER_MODEL), name, account_type (choices: checking/savings/cash/other), initial_balance (DecimalField 12,2 default 0), created_at, updated_at. Ordering by name.

URLs are mounted at `contas/` prefix in core/urls.py with app_name='accounts'. Route names: list, create, update, delete. Portuguese URL segments: `nova/`, `<pk>/editar/`, `<pk>/excluir/`.

Templates live in `templates/accounts/`: list.html, form.html, confirm_delete.html — all extending base_app.html using `{% block app_content %}`.

**Why:** Standard CRUD setup following project conventions.
**How to apply:** When adding features to accounts (e.g. current_balance, linking transactions), follow this same structure for any new views or template changes.
