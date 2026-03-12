---
name: transactions app architecture
description: Transaction model, form, views, and migration details for the transactions app (Sprint 6)
type: project
---

Transaction model lives in `transactions/models.py`. ForeignKeys to `accounts.Account` (CASCADE) and `categories.Category` (SET_NULL, nullable). `ordering = ['-date', '-created_at']`. Amount is always positive; `transaction_type` ('income'/'expense') defines the sign.

**Why:** Core financial data model linking users, accounts, and categories.

**How to apply:** When building list/filter views, filter by user and use `select_related('account', 'category')`. The form passes `user` via `__init__` to restrict account and category querysets. `TransactionListView.get_context_data` computes `total_income`, `total_expense`, and `balance` from the already-filtered queryset.
