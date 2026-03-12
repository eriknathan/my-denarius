## Lista de Tarefas — Sprints

---

### ✅ SPRINT 0 — Setup e Infraestrutura do Projeto

#### Tarefa 0.1 — Configuração do ambiente de desenvolvimento
- [X] 0.1.1 — Criar o virtualenv Python (`python -m venv .venv`)
- [X] 0.1.2 — Instalar Django (`pip install django`)
- [X] 0.1.3 — Criar o projeto Django com o nome `core` (`django-admin startproject core .`)
- [X] 0.1.4 — Criar o arquivo `requirements.txt` com as dependências iniciais
- [X] 0.1.5 — Criar o arquivo `.gitignore` com padrões Python/Django
- [X] 0.1.6 — Inicializar repositório Git (`git init` + primeiro commit)

#### Tarefa 0.2 — Criação das Django apps
- [X] 0.2.1 — Criar app `users` (`python manage.py startapp users`)
- [X] 0.2.2 — Criar app `profiles` (`python manage.py startapp profiles`)
- [X] 0.2.3 — Criar app `accounts` (`python manage.py startapp accounts`)
- [X] 0.2.4 — Criar app `categories` (`python manage.py startapp categories`)
- [X] 0.2.5 — Criar app `transactions` (`python manage.py startapp transactions`)
- [X] 0.2.6 — Registrar todas as apps em `INSTALLED_APPS` no `settings.py`

#### Tarefa 0.3 — Configuração do settings.py
- [X] 0.3.1 — Configurar `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`
- [X] 0.3.2 — Configurar `TEMPLATES` com `DIRS` apontando para a pasta `templates/` na raiz
- [X] 0.3.3 — Configurar `STATIC_URL` e `STATICFILES_DIRS`
- [X] 0.3.4 — Configurar `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL`
- [X] 0.3.5 — Configurar `AUTH_USER_MODEL = 'users.User'`
- [X] 0.3.6 — Configurar `AUTHENTICATION_BACKENDS` para o backend por e-mail

#### Tarefa 0.4 — Estrutura de templates e static
- [X] 0.4.1 — Criar pasta `templates/` na raiz do projeto
- [X] 0.4.2 — Criar subpastas: `templates/public/`, `templates/users/`, `templates/dashboard/`, `templates/accounts/`, `templates/categories/`, `templates/transactions/`, `templates/profiles/`, `templates/partials/`
- [X] 0.4.3 — Criar pasta `static/css/` na raiz do projeto
- [X] 0.4.4 - Crie os arquivos de .env e .env.example

#### Tarefa 0.5 — Configuração do TailwindCSS
- [X] 0.5.1 — Adicionar link do TailwindCSS CDN no `base.html` para desenvolvimento (`<script src="https://cdn.tailwindcss.com"></script>`)
- [X] 0.5.2 — Adicionar link da fonte Inter do Google Fonts no `base.html`
- [X] 0.5.3 — Documentar no README que o CDN é para dev e que CLI deve ser configurado antes do deploy

---

### ✅ SPRINT 1 — Model de Usuário e Autenticação

#### Tarefa 1.1 — Custom User Model (app `users`)
- [X] 1.1.1 — Criar `users/models.py` com a classe `User` herdando de `AbstractUser`
- [X] 1.1.2 — Definir `email` como campo obrigatório e único (`unique=True`)
- [X] 1.1.3 — Definir `username = None` para remover o campo username
- [X] 1.1.4 — Definir `USERNAME_FIELD = 'email'` e `REQUIRED_FIELDS = ['first_name', 'last_name']`
- [X] 1.1.5 — Adicionar campos `created_at = models.DateTimeField(auto_now_add=True)` e `updated_at = models.DateTimeField(auto_now=True)`
- [X] 1.1.6 — Criar e aplicar migration do model `User`

#### Tarefa 1.2 — Backend de autenticação por e-mail
- [X] 1.2.1 — Criar `users/backends.py` com classe `EmailBackend` herdando de `ModelBackend`
- [X] 1.2.2 — Implementar método `authenticate(request, username=None, password=None)` que busca por e-mail
- [X] 1.2.3 — Registrar o backend em `settings.py` em `AUTHENTICATION_BACKENDS`

#### Tarefa 1.3 — Formulários de autenticação (app `users`)
- [X] 1.3.1 — Criar `users/forms.py` com `UserRegistrationForm` herdando de `UserCreationForm`
- [X] 1.3.2 — Definir os campos: `first_name`, `last_name`, `email`, `password1`, `password2`
- [X] 1.3.3 — Criar `UserLoginForm` com campos `email` e `password`
- [X] 1.3.4 — Aplicar classes CSS do design system nos widgets dos campos dos formulários

#### Tarefa 1.4 — Views de autenticação (app `users`)
- [X] 1.4.1 — Criar `users/views.py` com `RegisterView` (CreateView ou FormView) para cadastro
- [X] 1.4.2 — Criar `LoginView` customizada (herdando de `django.contrib.auth.views.LoginView`) usando o form com e-mail
- [X] 1.4.3 — Criar `LogoutView` customizada (herdando de `django.contrib.auth.views.LogoutView`)
- [X] 1.4.4 — Configurar `success_url` do `RegisterView` para redirecionar ao dashboard

#### Tarefa 1.5 — URLs de autenticação
- [X] 1.5.1 — Criar `users/urls.py` com rotas: `register/`, `login/`, `logout/`
- [X] 1.5.2 — Incluir `users/urls.py` no `core/urls.py` com prefixo `''` (sem prefixo de path)

#### Tarefa 1.6 — Admin de usuários
- [X] 1.6.1 — Criar `users/admin.py` com `UserAdmin` customizado para exibir e-mail no lugar de username
- [X] 1.6.2 — Registrar o model `User` no admin com o `UserAdmin` customizado

---

### ✅ SPRINT 2 — Perfis, Templates Base e Site Público

#### Tarefa 2.1 — Model de Perfil (app `profiles`)
- [X] 2.1.1 — Criar `profiles/models.py` com classe `Profile`
- [X] 2.1.2 — Definir campo `user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
- [X] 2.1.3 — Definir campo `phone = models.CharField(max_length=20, blank=True)`
- [X] 2.1.4 — Adicionar `created_at` e `updated_at` com `auto_now_add` e `auto_now`
- [X] 2.1.5 — Criar e aplicar migration do model `Profile`
- [X] 2.1.6 — Registrar `Profile` no `profiles/admin.py`

#### Tarefa 2.2 — Signal de criação de perfil
- [X] 2.2.1 — Criar `profiles/signals.py`
- [X] 2.2.2 — Implementar signal `post_save` no model `User` para criar `Profile` automaticamente
- [X] 2.2.3 — Conectar o signal em `profiles/apps.py` no método `ready()`

#### Tarefa 2.3 — Template base (`base.html`)
- [X] 2.3.1 — Criar `templates/base.html` com estrutura HTML5 completa
- [X] 2.3.2 — Incluir link do TailwindCSS CDN e da fonte Inter
- [X] 2.3.3 — Definir blocos: `{% block title %}`, `{% block content %}`, `{% block extra_js %}`
- [X] 2.3.4 — Incluir `{% include 'partials/_messages.html' %}` no body

#### Tarefa 2.4 — Partial de mensagens
- [X] 2.4.1 — Criar `templates/partials/_messages.html` com loop `{% for message in messages %}`
- [X] 2.4.2 — Aplicar classes CSS condicionais por tipo de mensagem (success=verde, error=vermelho)

#### Tarefa 2.5 — Template base autenticado (com sidebar)
- [X] 2.5.1 — Criar `templates/base_app.html` herdando de `base.html`
- [X] 2.5.2 — Incluir `{% include 'partials/_sidebar.html' %}`
- [X] 2.5.3 — Definir área de conteúdo principal com padding e background gray-50

#### Tarefa 2.6 — Partial da sidebar
- [X] 2.6.1 — Criar `templates/partials/_sidebar.html` com estrutura da sidebar
- [X] 2.6.2 — Adicionar logo "my-denarius" com gradiente verde
- [X] 2.6.3 — Adicionar links de navegação: Dashboard, Contas, Categorias, Transações, Perfil
- [X] 2.6.4 — Adicionar link de Sair (logout) na parte inferior da sidebar
- [X] 2.6.5 — Marcar link ativo com `request.resolver_match.url_name` para highlight visual

#### Tarefa 2.7 — Site público (home)
- [X] 2.7.1 — Criar view `HomeView` (TemplateView) em um arquivo `views.py` na raiz ou app dedicado
- [X] 2.7.2 — Criar `templates/public/home.html` herdando de `base.html`
- [X] 2.7.3 — Implementar seção hero com gradiente verde e chamada para ação
- [X] 2.7.4 — Adicionar navbar pública com logo, botão "Entrar" e "Cadastre-se"
- [X] 2.7.5 — Adicionar seção de features/benefícios (3 cards simples)
- [X] 2.7.6 — Criar rota `''` (raiz) mapeada para `HomeView` em `core/urls.py`

#### Tarefa 2.8 — Templates de autenticação
- [X] 2.8.1 — Criar `templates/users/register.html` herdando de `base.html`
- [X] 2.8.2 — Renderizar o `UserRegistrationForm` com card centralizado e design do sistema
- [X] 2.8.3 — Criar `templates/users/login.html` herdando de `base.html`
- [X] 2.8.4 — Renderizar o `UserLoginForm` com card centralizado e design do sistema
- [X] 2.8.5 — Adicionar link "Não tem conta? Cadastre-se" na página de login
- [X] 2.8.6 — Adicionar link "Já tem conta? Entre" na página de cadastro

---

### ✅ SPRINT 3 — Dashboard

#### Tarefa 3.1 — View do Dashboard
- [X] 3.1.1 — Criar app ou view `dashboard` em `core/views.py` ou app dedicado
- [X] 3.1.2 — Criar `DashboardView` (LoginRequiredMixin + TemplateView)
- [X] 3.1.3 — Calcular e passar ao contexto: saldo total de todas as contas do usuário
- [X] 3.1.4 — Calcular e passar ao contexto: total de receitas do mês atual
- [X] 3.1.5 — Calcular e passar ao contexto: total de despesas do mês atual
- [X] 3.1.6 — Buscar e passar ao contexto: últimas 5 transações do usuário
- [X] 3.1.7 — Criar rota `dashboard/` em `core/urls.py` mapeada para `DashboardView`

#### Tarefa 3.2 — Template do Dashboard
- [X] 3.2.1 — Criar `templates/dashboard/index.html` herdando de `base_app.html`
- [X] 3.2.2 — Criar grid de 3 cards de métricas: Saldo Total, Receitas do Mês, Despesas do Mês
- [X] 3.2.3 — Aplicar cor verde para receitas e vermelho para despesas nos cards
- [X] 3.2.4 — Criar tabela com as últimas 5 transações (descrição, valor, tipo, data, conta)
- [X] 3.2.5 — Adicionar link "Ver todas as transações" abaixo da tabela
- [X] 3.2.6 — Exibir mensagem de boas-vindas com o nome do usuário logado

---

### ✅ SPRINT 4 — Contas Bancárias

#### Tarefa 4.1 — Model de Conta (app `accounts`)
- [X] 4.1.1 — Criar `accounts/models.py` com classe `Account`
- [X] 4.1.2 — Definir campo `user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
- [X] 4.1.3 — Definir `name = CharField(max_length=100)`
- [X] 4.1.4 — Definir `account_type = CharField(max_length=20, choices=[...])` com opções: Corrente, Poupança, Dinheiro, Outro
- [X] 4.1.5 — Definir `initial_balance = DecimalField(max_digits=12, decimal_places=2, default=0)`
- [X] 4.1.6 — Adicionar `created_at` e `updated_at`
- [X] 4.1.7 — Definir `__str__` retornando o nome da conta
- [X] 4.1.8 — Criar e aplicar migration

#### Tarefa 4.2 — Formulário de Conta
- [X] 4.2.1 — Criar `accounts/forms.py` com `AccountForm` (ModelForm)
- [X] 4.2.2 — Definir `fields = ['name', 'account_type', 'initial_balance']`
- [X] 4.2.3 — Aplicar classes CSS do design system nos widgets

#### Tarefa 4.3 — Views de Contas (CRUD)
- [X] 4.3.1 — Criar `accounts/views.py` com `AccountListView` (LoginRequiredMixin + ListView)
- [X] 4.3.2 — Filtrar queryset por `self.request.user` em `get_queryset()`
- [X] 4.3.3 — Criar `AccountCreateView` (LoginRequiredMixin + CreateView)
- [X] 4.3.4 — Sobrescrever `form_valid()` para associar `user = self.request.user`
- [X] 4.3.5 — Criar `AccountUpdateView` (LoginRequiredMixin + UpdateView)
- [X] 4.3.6 — Sobrescrever `get_queryset()` para filtrar por usuário (segurança)
- [X] 4.3.7 — Criar `AccountDeleteView` (LoginRequiredMixin + DeleteView)
- [X] 4.3.8 — Definir `success_url` para a listagem de contas

#### Tarefa 4.4 — URLs de Contas
- [X] 4.4.1 — Criar `accounts/urls.py` com rotas: `''` (list), `nova/` (create), `<pk>/editar/` (update), `<pk>/excluir/` (delete)
- [X] 4.4.2 — Incluir `accounts/urls.py` em `core/urls.py` com prefixo `contas/`

#### Tarefa 4.5 — Templates de Contas
- [X] 4.5.1 — Criar `templates/accounts/list.html` com tabela de contas e botões de ação
- [X] 4.5.2 — Adicionar botão "Nova Conta" no topo da listagem
- [X] 4.5.3 — Criar `templates/accounts/form.html` para criação e edição (mesmo template)
- [X] 4.5.4 — Criar `templates/accounts/confirm_delete.html` com mensagem de confirmação

#### Tarefa 4.6 — Admin de Contas
- [X] 4.6.1 — Registrar `Account` em `accounts/admin.py` com `list_display = ['name', 'user', 'account_type', 'initial_balance']`

---

### ✅ SPRINT 5 — Categorias

#### Tarefa 5.1 — Model de Categoria (app `categories`)
- [X] 5.1.1 — Criar `categories/models.py` com classe `Category`
- [X] 5.1.2 — Definir `user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
- [X] 5.1.3 — Definir `name = CharField(max_length=100)`
- [X] 5.1.4 — Definir `category_type = CharField(max_length=10, choices=[('income', 'Receita'), ('expense', 'Despesa')])`
- [X] 5.1.5 — Adicionar `created_at` e `updated_at`
- [X] 5.1.6 — Definir `__str__` retornando `nome (tipo)`
- [X] 5.1.7 — Criar e aplicar migration

#### Tarefa 5.2 — Formulário de Categoria
- [X] 5.2.1 — Criar `categories/forms.py` com `CategoryForm` (ModelForm)
- [X] 5.2.2 — Definir `fields = ['name', 'category_type']`
- [X] 5.2.3 — Aplicar classes CSS do design system nos widgets

#### Tarefa 5.3 — Views de Categorias (CRUD)
- [X] 5.3.1 — Criar `CategoryListView` (LoginRequiredMixin + ListView) filtrando por usuário
- [X] 5.3.2 — Criar `CategoryCreateView` associando usuário no `form_valid()`
- [X] 5.3.3 — Criar `CategoryUpdateView` filtrando por usuário no `get_queryset()`
- [X] 5.3.4 — Criar `CategoryDeleteView` com `success_url` para listagem

#### Tarefa 5.4 — URLs de Categorias
- [X] 5.4.1 — Criar `categories/urls.py` com rotas CRUD
- [X] 5.4.2 — Incluir em `core/urls.py` com prefixo `categorias/`

#### Tarefa 5.5 — Templates de Categorias
- [X] 5.5.1 — Criar `templates/categories/list.html` com tabela e badge de tipo (receita=verde, despesa=vermelho)
- [X] 5.5.2 — Criar `templates/categories/form.html`
- [X] 5.5.3 — Criar `templates/categories/confirm_delete.html`

#### Tarefa 5.6 — Admin de Categorias
- [X] 5.6.1 — Registrar `Category` em `categories/admin.py`

---

### ✅ SPRINT 6 — Transações

#### Tarefa 6.1 — Model de Transação (app `transactions`)
- [X] 6.1.1 — Criar `transactions/models.py` com classe `Transaction`
- [X] 6.1.2 — Definir `user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
- [X] 6.1.3 — Definir `account = ForeignKey('accounts.Account', on_delete=CASCADE)`
- [X] 6.1.4 — Definir `category = ForeignKey('categories.Category', on_delete=SET_NULL, null=True, blank=True)`
- [X] 6.1.5 — Definir `description = CharField(max_length=200)`
- [X] 6.1.6 — Definir `amount = DecimalField(max_digits=12, decimal_places=2)`
- [X] 6.1.7 — Definir `transaction_type = CharField(choices=[('income', 'Receita'), ('expense', 'Despesa')])`
- [X] 6.1.8 — Definir `date = DateField()`
- [X] 6.1.9 — Definir `notes = TextField(blank=True)`
- [X] 6.1.10 — Adicionar `created_at` e `updated_at`
- [X] 6.1.11 — Definir `class Meta: ordering = ['-date', '-created_at']`
- [X] 6.1.12 — Criar e aplicar migration

#### Tarefa 6.2 — Formulário de Transação
- [X] 6.2.1 — Criar `transactions/forms.py` com `TransactionForm` (ModelForm)
- [X] 6.2.2 — Definir todos os campos relevantes
- [X] 6.2.3 — Filtrar queryset de `account` e `category` pelo `user` no `__init__` do form
- [X] 6.2.4 — Aplicar classes CSS do design system nos widgets
- [X] 6.2.5 — Configurar widget de data como `type="date"`

#### Tarefa 6.3 — Views de Transações (CRUD)
- [X] 6.3.1 — Criar `TransactionListView` (LoginRequiredMixin + ListView) com filtros via GET params
- [X] 6.3.2 — Implementar filtragem por: `date_start`, `date_end`, `transaction_type`, `account`, `category`
- [X] 6.3.3 — Passar totais filtrados (receitas, despesas) ao contexto
- [X] 6.3.4 — Usar `select_related('account', 'category')` na queryset
- [X] 6.3.5 — Criar `TransactionCreateView` com `form_valid()` associando usuário
- [X] 6.3.6 — Criar `TransactionUpdateView` filtrando por usuário
- [X] 6.3.7 — Criar `TransactionDeleteView` com `success_url` para listagem

#### Tarefa 6.4 — URLs de Transações
- [X] 6.4.1 — Criar `transactions/urls.py` com rotas CRUD
- [X] 6.4.2 — Incluir em `core/urls.py` com prefixo `transacoes/`

#### Tarefa 6.5 — Templates de Transações
- [X] 6.5.1 — Criar `templates/transactions/list.html` com tabela de transações
- [X] 6.5.2 — Adicionar formulário de filtros (período, tipo, conta, categoria) acima da tabela
- [X] 6.5.3 — Colorir valor: verde para receitas, vermelho para despesas
- [X] 6.5.4 — Exibir totais de receitas e despesas filtradas abaixo ou acima da tabela
- [X] 6.5.5 — Criar `templates/transactions/form.html`
- [X] 6.5.6 — Criar `templates/transactions/confirm_delete.html`

#### Tarefa 6.6 — Admin de Transações
- [X] 6.6.1 — Registrar `Transaction` em `transactions/admin.py` com `list_display` e `list_filter`

---

### ✅ SPRINT 7 — Perfil do Usuário

#### Tarefa 7.1 — View de Perfil
- [X] 7.1.1 — Criar `profiles/views.py` com `ProfileDetailView` (LoginRequiredMixin + DetailView)
- [X] 7.1.2 — Sobrescrever `get_object()` para retornar `request.user.profile`
- [X] 7.1.3 — Criar `ProfileUpdateView` (LoginRequiredMixin + UpdateView) para edição do perfil e dados do usuário
- [X] 7.1.4 — Criar `profiles/forms.py` com `ProfileForm` (campos de `Profile`) e `UserUpdateForm` (campos de `User`: `first_name`, `last_name`)

#### Tarefa 7.2 — URLs de Perfil
- [X] 7.2.1 — Criar `profiles/urls.py` com rotas: `''` (detail), `editar/` (update)
- [X] 7.2.2 — Incluir em `core/urls.py` com prefixo `perfil/`

#### Tarefa 7.3 — Templates de Perfil
- [X] 7.3.1 — Criar `templates/profiles/detail.html` exibindo dados do usuário e perfil
- [X] 7.3.2 — Criar `templates/profiles/form.html` para edição com dois formulários no mesmo template

---

### ✅ SPRINT 8 — Polimento, Ajustes e README

#### Tarefa 8.1 — Revisão do design system
- [X] 8.1.1 — Revisar todos os templates e garantir consistência visual
- [X] 8.1.2 — Verificar responsividade em mobile (320px) e desktop (1280px+)
- [X] 8.1.3 — Garantir que todos os formulários exibem erros de validação com estilo correto
- [X] 8.1.4 — Verificar se as mensagens Django (success/error) aparecem em todas as ações

#### Tarefa 8.2 — Segurança e edge cases
- [X] 8.2.1 — Verificar que todas as views protegidas usam `LoginRequiredMixin`
- [X] 8.2.2 — Verificar que todos os querysets filtram por `request.user`
- [X] 8.2.3 — Testar acesso a recursos de outro usuário via URL direta (deve retornar 404)
- [X] 8.2.4 — Verificar que o `{% csrf_token %}` está em todos os formulários

#### Tarefa 8.3 — Configuração do admin
- [X] 8.3.1 — Verificar registro de todos os models no admin
- [X] 8.3.2 — Configurar `list_display` e `list_filter` relevantes em cada admin
- [X] 8.3.3 — Criar superusuário padrão para dev (`python manage.py createsuperuser`)

#### Tarefa 8.4 — README do projeto
- [X] 8.4.1 — Criar `README.md` na raiz do projeto
- [X] 8.4.2 — Documentar: visão geral, requisitos, instalação passo a passo
- [X] 8.4.3 — Documentar: como rodar o projeto em desenvolvimento
- [X] 8.4.4 — Documentar: estrutura de diretórios e apps
- [X] 8.4.5 — Documentar: decisões técnicas (login por e-mail, custom user model)

---

### 🏃 SPRINT 9 (FINAL) — Testes e Docker *(sprints finais)*

#### Tarefa 9.1 — Configuração de testes
- [ ] 9.1.1 — Configurar `pytest-django` ou usar `unittest` nativo do Django
- [ ] 9.1.2 — Criar testes de model para `User`, `Profile`, `Account`, `Category`, `Transaction`
- [ ] 9.1.3 — Criar testes de view para autenticação (cadastro, login, logout)
- [ ] 9.1.4 — Criar testes de view para CRUD de contas, categorias e transações
- [ ] 9.1.5 — Criar testes de segurança (acesso a dados de outro usuário)

#### Tarefa 9.2 — Docker
- [ ] 9.2.1 — Criar `Dockerfile` para a aplicação Django
- [ ] 9.2.2 — Criar `docker-compose.yml` com serviço `web`
- [ ] 9.2.3 — Configurar variáveis de ambiente via `ENV` / `.env`
- [ ] 9.2.4 — Configurar TailwindCSS CLI para compilar em produção
- [ ] 9.2.5 — Documentar no README como rodar com Docker
