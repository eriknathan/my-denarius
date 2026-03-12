# Setup e Desenvolvimento

## Pré-requisitos

- Python 3.12+
- pip
- Git

---

## Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd my-denarius

# 2. Crie e ative o virtualenv
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Configuração inicial

Antes de rodar o projeto pela primeira vez, confirme que `core/settings.py` tem:

```python
AUTH_USER_MODEL = 'users.User'
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
TEMPLATES = [{'DIRS': [BASE_DIR / 'templates'], ...}]
```

> Atenção: `AUTH_USER_MODEL` deve estar definido **antes** de criar as migrations.

---

## Rodando o projeto

```bash
# Aplicar migrations
python manage.py migrate

# Criar superusuário para o admin
python manage.py createsuperuser

# Iniciar o servidor de desenvolvimento
python manage.py runserver
```

O projeto estará disponível em `http://127.0.0.1:8000`.
O admin Django em `http://127.0.0.1:8000/admin/`.

---

## Comandos do dia a dia

```bash
# Criar migrations após alterar um model
python manage.py makemigrations

# Aplicar migrations pendentes
python manage.py migrate

# Abrir o shell do Django
python manage.py shell

# Verificar problemas de configuração
python manage.py check

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

---

## Adicionando uma nova app

```bash
python manage.py startapp nome_da_app
```

Depois registrar em `core/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'nome_da_app',
]
```

---

## Estrutura de uma nova app

Toda app do projeto segue esta estrutura:

```
nome_da_app/
├── migrations/
│   └── __init__.py
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

---

## Dependências

| Pacote | Versão |
|---|---|
| Django | 6.0.3 |
| asgiref | 3.11.1 |
| sqlparse | 0.5.5 |

Para adicionar uma dependência:

```bash
pip install nome-do-pacote
pip freeze > requirements.txt
```

---

## TailwindCSS

No desenvolvimento, o TailwindCSS é carregado via CDN — nenhuma configuração extra necessária.

```html
<!-- base.html -->
<script src="https://cdn.tailwindcss.com"></script>
```

> Para produção, será necessário configurar o Tailwind CLI para gerar o `output.css` compilado. Isso está planejado para as sprints finais junto com Docker.
