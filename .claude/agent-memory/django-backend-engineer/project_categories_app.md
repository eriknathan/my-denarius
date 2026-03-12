---
name: categories app architecture
description: Category model, form, views, URLs, admin, and templates for the categories app
type: project
---

Model `Category` em `categories/models.py`:
- `user` ForeignKey → `settings.AUTH_USER_MODEL`, `related_name='categories'`
- `name` CharField(100)
- `category_type` CharField(10), choices: `('income', 'Receita')`, `('expense', 'Despesa')`
- `created_at`, `updated_at`
- `__str__` retorna `f'{self.name} ({self.get_category_type_display()})'`
- `Meta.ordering = ['name']`, verbose_name em português

Form `CategoryForm` em `categories/forms.py`:
- fields: `['name', 'category_type']`
- INPUT_CLASS compartilhado com o padrão do accounts app

Views em `categories/views.py`:
- `CategoryListView` — ListView, filtra por `request.user`
- `CategoryCreateView` — associa `user` em `form_valid()`
- `CategoryUpdateView` — `get_queryset()` filtra por `request.user`
- `CategoryDeleteView` — `get_queryset()` filtra por `request.user`

URLs em `categories/urls.py` (app_name = 'categories'):
- `''` → list
- `nova/` → create
- `<int:pk>/editar/` → update
- `<int:pk>/excluir/` → delete

Incluído em `core/urls.py` com prefixo `categorias/`.

Templates em `templates/categories/`:
- `list.html` — exibe tipo com cor (emerald-600 para receita, red-500 para despesa)
- `form.html` — formulário compartilhado para criar/editar
- `confirm_delete.html` — confirmação de exclusão

Admin registrado com `list_display`, `list_filter` e `search_fields`.
Migration `0001_initial` aplicada com sucesso.

**Why:** sprint 5 do projeto my-denarius — CRUD de categorias por usuário.
**How to apply:** seguir este mesmo padrão ao implementar o app transactions.
