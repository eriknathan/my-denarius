# my-denarius

Sistema de gestão de finanças pessoais construído com Django.

## Requisitos

- Python 3.12+
- pip

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositório>
cd my-denarius

# Crie e ative o virtualenv
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Aplique as migrations
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser
```

## Rodando em desenvolvimento

```bash
source venv/bin/activate
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000

## Estrutura de diretórios

```
my-denarius/
├── core/               # Configurações do projeto (settings.py, urls.py)
├── users/              # Custom User Model (autenticação por e-mail)
├── profiles/           # Perfil 1:1 com usuário
├── accounts/           # Contas bancárias
├── categories/         # Categorias de receitas/despesas
├── transactions/       # Transações financeiras
├── templates/          # Templates HTML centralizados
│   ├── base.html
│   ├── base_app.html
│   ├── public/
│   ├── users/
│   ├── dashboard/
│   ├── accounts/
│   ├── categories/
│   ├── transactions/
│   ├── profiles/
│   └── partials/
├── static/             # Arquivos estáticos
│   └── css/
├── docs/               # Documentação do projeto
└── manage.py
```

## Decisões técnicas

### Login por e-mail

O projeto usa um `Custom User Model` (`users.User`) com `email` como campo de login (`USERNAME_FIELD = 'email'`). O campo `username` foi removido. A autenticação é feita via `EmailBackend` customizado em `users/backends.py`.

### TailwindCSS via CDN

Em desenvolvimento, o TailwindCSS é carregado via CDN (`https://cdn.tailwindcss.com`) — sem build step necessário. **Antes do deploy em produção**, o TailwindCSS CLI deve ser configurado para gerar um arquivo CSS otimizado e minificado, substituindo o CDN.

### SQLite

O banco de dados padrão é SQLite (`db.sqlite3`), adequado para desenvolvimento. Em produção, recomenda-se PostgreSQL.
