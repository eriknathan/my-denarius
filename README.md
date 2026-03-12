# my-denarius

Sistema de gestão de finanças pessoais construído com Django full stack. Permite registrar, categorizar e acompanhar receitas e despesas organizadas por contas bancárias e categorias personalizáveis.

> *"Denarius"* é uma moeda romana antiga — o nome reforça a ideia de controle e valor do dinheiro ao longo do tempo.

---

## Visão Geral

O **my-denarius** é uma aplicação web que oferece:

- **Dashboard** com resumo financeiro: saldo total, receitas e despesas do mês
- **Contas bancárias**: corrente, poupança, dinheiro e outros tipos
- **Categorias** personalizáveis por tipo (receita ou despesa)
- **Transações** com filtros por período, tipo, conta e categoria
- **Perfil do usuário** com dados pessoais editáveis
- **Autenticação por e-mail** (sem campo username)

---

## Requisitos

- Python 3.12+
- pip

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositório>
cd my-denarius

# 2. Crie e ative o virtualenv
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e defina pelo menos: SECRET_KEY e DEBUG

# 5. Aplique as migrations
python manage.py migrate

# 6. (Opcional) Crie um superusuário para acessar o admin
python manage.py createsuperuser
```

---

## Rodando em desenvolvimento

```bash
source venv/bin/activate
python manage.py runserver
```

Acesse a aplicação em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

O Django Admin está disponível em: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Estrutura de diretórios

```
my-denarius/
├── core/                   # Configurações do projeto
│   ├── settings.py         # Configurações Django
│   ├── urls.py             # URLs raiz
│   └── views.py            # DashboardView
│
├── users/                  # Custom User Model e autenticação
│   ├── models.py           # User com email como campo de login
│   ├── backends.py         # EmailBackend customizado
│   ├── forms.py            # UserRegistrationForm, UserLoginForm
│   ├── views.py            # RegisterView, LoginView, LogoutView
│   └── urls.py
│
├── profiles/               # Perfil 1:1 com usuário
│   ├── models.py           # Profile (phone)
│   ├── signals.py          # Cria Profile automaticamente via post_save
│   ├── forms.py            # ProfileForm, UserUpdateForm
│   └── views.py            # ProfileDetailView, ProfileUpdateView
│
├── accounts/               # Contas bancárias
│   ├── models.py           # Account (corrente, poupança, dinheiro, outro)
│   ├── forms.py            # AccountForm
│   └── views.py            # CRUD completo
│
├── categories/             # Categorias de receitas/despesas
│   ├── models.py           # Category (income/expense)
│   ├── forms.py            # CategoryForm
│   └── views.py            # CRUD completo
│
├── transactions/           # Transações financeiras
│   ├── models.py           # Transaction (vinculada a conta e categoria)
│   ├── forms.py            # TransactionForm com querysets por usuário
│   └── views.py            # CRUD + filtros
│
├── templates/              # Templates HTML centralizados
│   ├── base.html           # Layout base (HTML5 + TailwindCSS + Inter)
│   ├── base_app.html       # Layout autenticado (com sidebar)
│   ├── public/             # Página pública (home)
│   ├── users/              # Login e cadastro
│   ├── dashboard/          # Dashboard
│   ├── accounts/           # CRUD de contas
│   ├── categories/         # CRUD de categorias
│   ├── transactions/       # CRUD de transações
│   ├── profiles/           # Detalhe e edição de perfil
│   └── partials/           # Sidebar, mensagens
│
├── static/                 # Arquivos estáticos
│   └── css/
│
├── docs/                   # Documentação técnica do projeto
│   ├── architecture.md
│   ├── models.md
│   ├── conventions.md
│   └── design-system.md
│
├── agents/                 # Instruções para agentes de IA
│   ├── backend.md
│   ├── frontend.md
│   └── qa.md
│
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt
└── manage.py
```

---

## URLs da aplicação

| URL | Descrição |
|-----|-----------|
| `/` | Página pública |
| `/register/` | Cadastro de usuário |
| `/login/` | Login |
| `/logout/` | Logout |
| `/dashboard/` | Dashboard (requer login) |
| `/contas/` | Listagem de contas |
| `/categorias/` | Listagem de categorias |
| `/transacoes/` | Listagem de transações com filtros |
| `/perfil/` | Detalhe do perfil |
| `/perfil/editar/` | Edição do perfil |
| `/admin/` | Django Admin |

---

## Decisões técnicas

### Autenticação por e-mail (sem username)

O projeto usa um `Custom User Model` (`users.User`) com `email` como campo de login (`USERNAME_FIELD = 'email'`). O campo `username` foi removido (`username = None`). A autenticação é feita via `EmailBackend` customizado em `users/backends.py`, que busca o usuário pelo e-mail em vez do username padrão do Django.

Essa decisão foi tomada pois e-mail é um identificador mais natural e menos propenso a duplicatas ou esquecimento.

### Isolamento de dados por usuário

Todas as views autenticadas usam `LoginRequiredMixin` e todos os `get_queryset()` filtram por `request.user`. Isso garante que um usuário nunca acessa dados de outro — tentativas de acesso via URL direta resultam em 404.

### Templates centralizados

Todos os templates ficam em `templates/` na raiz do projeto (não dentro das apps). Isso simplifica a organização e evita duplicação. A hierarquia é: `base.html` → `base_app.html` → páginas específicas.

### TailwindCSS via CDN

Em desenvolvimento, o TailwindCSS é carregado via CDN (`https://cdn.tailwindcss.com`) sem build step necessário. **Antes do deploy em produção**, o TailwindCSS CLI deve ser configurado para gerar um arquivo CSS otimizado e minificado, substituindo o CDN.

### SQLite

O banco de dados padrão é SQLite (`db.sqlite3`), adequado para desenvolvimento e projetos pessoais. Para ambientes de produção com múltiplos usuários, recomenda-se PostgreSQL.

### Signals para criação de perfil

O `Profile` de cada usuário é criado automaticamente via signal `post_save` no model `User`, implementado em `profiles/signals.py` e conectado no `ProfilesConfig.ready()`. Isso garante que todo usuário registrado já tenha um perfil disponível.

---

## Stack

| Camada | Tecnologia |
|--------|------------|
| Linguagem | Python 3.12+ |
| Framework | Django 5.x |
| Frontend | Django Template Language |
| CSS | TailwindCSS via CDN |
| Fonte | Inter (Google Fonts) |
| Banco de dados | SQLite |
| Autenticação | Django Auth com EmailBackend customizado |

---

## Documentação adicional

A pasta `docs/` contém os guidelines completos do projeto:

- [`docs/architecture.md`](docs/architecture.md) — mapa de URLs e decisões de arquitetura
- [`docs/models.md`](docs/models.md) — campos e relacionamentos de todos os models
- [`docs/conventions.md`](docs/conventions.md) — exemplos de código (models, views, forms, signals)
- [`docs/design-system.md`](docs/design-system.md) — componentes HTML prontos com classes Tailwind
