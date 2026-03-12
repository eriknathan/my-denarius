# Arquitetura do Projeto

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Framework | Django 6.x |
| Frontend | Django Template Language + TailwindCSS (CDN no dev) |
| Banco de dados | SQLite (padrão Django) |
| Autenticação | Django Auth nativo com backend customizado por e-mail |

---

## Estrutura de diretórios

```
my-denarius/
├── accounts/               # App: contas bancárias
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── categories/             # App: categorias de transações
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── core/                   # Configurações globais
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── profiles/               # App: perfis de usuários
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── transactions/           # App: transações financeiras
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── users/                  # App: usuário customizado
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/              # Templates centralizados
│   ├── base.html
│   ├── base_app.html
│   ├── partials/
│   │   ├── _sidebar.html
│   │   └── _messages.html
│   ├── public/
│   │   └── home.html
│   ├── users/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   └── index.html
│   ├── accounts/
│   ├── categories/
│   ├── transactions/
│   └── profiles/
├── static/
│   └── css/
├── docs/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## Apps e responsabilidades

| App | Responsabilidade |
|---|---|
| `core` | Configurações globais, URL raiz, ponto de entrada da aplicação |
| `users` | Custom User Model, backend de autenticação por e-mail, views de cadastro e login |
| `profiles` | Perfil estendido do usuário (1:1 com User), criado automaticamente via signal |
| `accounts` | CRUD de contas bancárias vinculadas ao usuário |
| `categories` | CRUD de categorias de receitas e despesas vinculadas ao usuário |
| `transactions` | CRUD de transações financeiras com filtros, vinculadas a conta e categoria |

---

## Mapa de URLs

| Prefixo | App | Rotas internas |
|---|---|---|
| `/` | `core` | home (pública) |
| `/admin/` | Django admin | — |
| `/register/` | `users` | cadastro |
| `/login/` | `users` | login |
| `/logout/` | `users` | logout |
| `/dashboard/` | `core` ou view dedicada | dashboard principal |
| `/contas/` | `accounts` | list, create, update, delete |
| `/categorias/` | `categories` | list, create, update, delete |
| `/transacoes/` | `transactions` | list, create, update, delete |
| `/perfil/` | `profiles` | detail, update |

---

## Fluxo de autenticação

```
Acesso → Página Pública
    ├── Cadastro → perfil criado via signal → Dashboard
    └── Login (e-mail + senha) → EmailBackend → Dashboard

Qualquer rota protegida sem sessão → redirect para /login/
```

---

## Decisões técnicas

**Login por e-mail, não por username**
`USERNAME_FIELD = 'email'` no model `User`. Um `EmailBackend` em `users/backends.py` faz a busca por e-mail no `authenticate()`.

**Custom User Model antes da primeira migration**
`AUTH_USER_MODEL = 'users.User'` deve estar em `settings.py` antes de qualquer `migrate`. Alterar depois quebra o banco.

**Signals em arquivo próprio**
Signals ficam em `<app>/signals.py` e são registrados no `ready()` do `AppConfig` da app, não no `models.py`.

**Templates centralizados na raiz**
`TEMPLATES[0]['DIRS']` aponta para `BASE_DIR / 'templates'`. Nenhum template fica dentro das apps.

**Isolamento de dados por usuário**
Todos os querysets filtram por `request.user`. Views de update e delete sobrescrevem `get_queryset()` para garantir que um usuário não acesse recursos de outro.
