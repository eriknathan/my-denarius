# Padrões de Código

## Regras gerais

- **PEP8** rigorosamente — sem warnings
- **Aspas simples** em todo o código Python
- Nomes de variáveis, funções e classes em **inglês**
- Textos da interface (labels, mensagens, placeholders) em **português brasileiro**
- Preferir **Class Based Views** — usar `as_view()` nas URLs
- Sem over-engineering: implementar apenas o que foi solicitado

---

## Models

Todo model deve herdar de `models.Model` e ter os campos de auditoria:

```python
class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
```

Regras:
- `created_at` e `updated_at` obrigatórios em todos os models
- `__str__` obrigatório em todos os models
- `class Meta` com `ordering` sempre que fizer sentido
- ForeignKeys para `User` usam `settings.AUTH_USER_MODEL`, nunca `get_user_model()` direto no campo

---

## Views

Padrão para views protegidas (CRUD):

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Account
from .forms import AccountForm


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/confirm_delete.html'
    success_url = reverse_lazy('accounts:list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
```

Regras:
- Sempre usar `LoginRequiredMixin` em views da área autenticada
- Sempre sobrescrever `get_queryset()` nas views de update e delete para filtrar por `request.user`
- Associar `user` ao objeto no `form_valid()` das views de criação
- Usar `reverse_lazy()` no `success_url` (não `reverse()`)
- Usar `select_related('account', 'category')` quando houver ForeignKeys no queryset

---

## Forms

```python
from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'initial_balance']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg '
                         'text-sm text-gray-800 placeholder-gray-400 '
                         'focus:outline-none focus:ring-2 focus:ring-emerald-500 '
                         'focus:border-emerald-500 transition-colors duration-200',
                'placeholder': 'Nome da conta',
            }),
        }
```

Regras:
- Sempre usar `ModelForm`
- Aplicar as classes CSS do design system nos `widgets`
- Forms que dependem do usuário logado (ex: filtrar contas por usuário) recebem `user` no `__init__`:

```python
def __init__(self, *args, user=None, **kwargs):
    super().__init__(*args, **kwargs)
    if user:
        self.fields['account'].queryset = Account.objects.filter(user=user)
```

---

## URLs

Cada app tem seu próprio `urls.py` com `app_name` definido:

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountListView.as_view(), name='list'),
    path('nova/', views.AccountCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.AccountUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.AccountDeleteView.as_view(), name='delete'),
]
```

Incluídos no `core/urls.py`:

```python
path('contas/', include('accounts.urls')),
```

Referência nas templates com namespace:

```html
{% url 'accounts:list' %}
{% url 'accounts:update' account.pk %}
```

---

## Signals

```python
# profiles/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

```python
# profiles/apps.py
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals  # noqa: F401
```

---

## Templates

Hierarquia de herança:

```
base.html                   ← HTML base, TailwindCSS, Inter, bloco title/content
└── base_app.html           ← inclui sidebar, layout autenticado
    └── dashboard/index.html, accounts/list.html, ...

base.html
└── public/home.html
└── users/login.html
└── users/register.html
```

Padrão de template de listagem:

```html
{% extends 'base_app.html' %}

{% block title %}Contas{% endblock %}

{% block content %}
<div class="p-6">
  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-gray-800">Contas</h1>
    <a href="{% url 'accounts:create' %}" class="...botão primário...">Nova Conta</a>
  </div>

  {% include 'partials/_messages.html' %}

  <!-- tabela -->
</div>
{% endblock %}
```

Regras:
- Todo formulário deve ter `{% csrf_token %}`
- Partials com prefixo `_` em `templates/partials/`
- Link ativo na sidebar via `request.resolver_match.url_name`
- Erros de campo: `{{ form.field.errors.0 }}` com classe `text-xs text-red-500`
