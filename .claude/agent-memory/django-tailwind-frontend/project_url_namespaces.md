---
name: URL namespace conventions
description: App namespace names and key URL patterns used in templates for this project
type: project
---

URL namespaces confirmed or planned for my-denarius templates:

| App | app_name | Key URL names |
|-----|----------|--------------|
| users | `users` | `users:login`, `users:logout`, `users:register` |
| dashboard | `dashboard` | `dashboard:index` |
| accounts | `accounts` | `accounts:list`, `accounts:create`, `accounts:update`, `accounts:delete` |
| categories | `categories` | `categories:list`, `categories:create`, `categories:update`, `categories:delete` |
| transactions | `transactions` | `transactions:list`, `transactions:create`, `transactions:update`, `transactions:delete` |
| profiles | `profiles` | `profiles:detail`, `profiles:update` |

Non-namespaced URLs (from core/urls.py):
- `home` — public landing page

**Why:** Only `users` app has its `urls.py` confirmed. The other app namespaces are based on `docs/architecture.md` planned structure. Another agent is wiring these into `core/urls.py`.

**How to apply:** Always use namespaced URL tags in templates. For `home`, use `{% url 'home' %}` (no namespace). Sidebar active state check: `request.resolver_match.app_name == '<app_name>'`.
