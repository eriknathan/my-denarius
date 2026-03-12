# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos

```bash
# Ativar o virtualenv
source venv/bin/activate

# Rodar o servidor
python manage.py runserver

# Criar e aplicar migrations
python manage.py makemigrations
python manage.py migrate

# Verificar configuração
python manage.py check

# Shell interativo
python manage.py shell
```

## Arquitetura

O projeto é um Django full stack chamado **my-denarius** (gestão de finanças pessoais). O pacote de configurações principal chama-se `core` (não `config` nem o nome do projeto).

**Apps e domínios:**
- `users` — Custom User Model com `email` como `USERNAME_FIELD` (`username = None`). Contém também `backends.py` com `EmailBackend` para autenticação por e-mail.
- `profiles` — Perfil 1:1 com User, criado via signal `post_save` em `profiles/signals.py`, conectado no `ProfilesConfig.ready()`.
- `accounts` — Contas bancárias do usuário (corrente, poupança, dinheiro, outro).
- `categories` — Categorias de receitas/despesas (`income`/`expense`) por usuário.
- `transactions` — Transações financeiras vinculadas a conta e categoria, com `ordering = ['-date', '-created_at']`.
- `core` — `settings.py`, `urls.py` raiz, sem models próprios.

**Templates:** centralizados em `templates/` na raiz (não dentro das apps). `base.html` e `base_app.html` (com sidebar) são os dois layouts base.

**URLs:** cada app tem `app_name` definido e é incluída em `core/urls.py` com prefixo em português (`contas/`, `categorias/`, `transacoes/`, `perfil/`). Users sem prefixo.

## Padrões obrigatórios

- **Aspas simples** em todo o Python
- **CBVs** com `LoginRequiredMixin` em todas as views da área autenticada
- `get_queryset()` sempre filtra por `request.user` — nas views de update e delete também
- Todo model tem `created_at` (`auto_now_add`) e `updated_at` (`auto_now`)
- Signals ficam em `<app>/signals.py`, nunca em `models.py`
- Todo formulário no template tem `{% csrf_token %}`
- `reverse_lazy()` no `success_url` das CBVs
- `select_related` nas querysets que acessam ForeignKeys

## Settings relevantes a configurar

```python
AUTH_USER_MODEL = 'users.User'          # antes da primeira migration
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
TEMPLATES = [{'DIRS': [BASE_DIR / 'templates'], ...}]
AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']
```

## Design

TailwindCSS via CDN (`https://cdn.tailwindcss.com`) — sem build step no desenvolvimento. Fonte Inter via Google Fonts. Cor primária: `emerald-600`. Receitas em `emerald-600`, despesas em `red-500`. Ver `docs/design-system.md` para componentes prontos.

## Documentação

A pasta `docs/` contém os guidelines completos do projeto:
- `architecture.md` — mapa de URLs, decisões técnicas
- `models.md` — campos e relacionamentos de todos os models
- `conventions.md` — exemplos de código para models, views, forms, signals
- `design-system.md` — componentes HTML prontos com classes Tailwind
