# Agentes de IA — my-denarius

Time de agentes especializados no desenvolvimento do **my-denarius** (sistema de gestão de finanças pessoais em Django).

Cada agente é um arquivo `.md` com instruções específicas de papel, responsabilidades, padrões do projeto e ferramentas a usar.

---

## Índice de agentes

| Arquivo | Agente | Quando usar |
|---|---|---|
| [backend.md](./backend.md) | Django Backend Engineer | Models, views, forms, URLs, signals, migrations, admin |
| [frontend.md](./frontend.md) | Frontend Engineer | Templates Django, componentes TailwindCSS, layouts, partials |
| [qa.md](./qa.md) | QA Engineer | Testes funcionais no browser, validação de design e segurança |

---

## Descrições

### Django Backend Engineer — `backend.md`

**Especialidade:** Python 3.12, Django 6.x, ORM, CBVs, autenticação, signals, formulários, admin.

**Responsabilidades:**
- Criar e manter models com migrations
- Implementar Class Based Views com `LoginRequiredMixin`
- Escrever forms com `ModelForm` e widgets estilizados
- Configurar URLs com namespaces
- Implementar signals em `signals.py`
- Garantir isolamento de dados por `request.user`
- Configurar o Django Admin

**Ferramenta MCP:** `context7` — para consultar documentação atualizada do Django (ORM, CBVs, signals, autenticação, admin).

**Quando usar:**
- Criar ou alterar um model
- Implementar um novo CRUD de uma app
- Resolver bugs de backend (queries, formulários, autenticação)
- Configurar `settings.py`
- Escrever signals ou backends customizados

---

### Frontend Engineer — `frontend.md`

**Especialidade:** Django Template Language, TailwindCSS (via CDN), design system do projeto.

**Responsabilidades:**
- Criar e manter templates HTML com DTL
- Aplicar o design system (cores, botões, inputs, cards, tabelas)
- Manter a hierarquia de templates (`base.html` → `base_app.html` → páginas)
- Construir e manter a sidebar e partials
- Garantir responsividade (mobile e desktop)
- Renderizar formulários com estilos corretos e mensagens de erro

**Ferramenta MCP:** `context7` — para consultar classes TailwindCSS e tags/filters do Django Template Language.

**Quando usar:**
- Criar ou ajustar um template HTML
- Implementar um novo componente visual (card, tabela, formulário)
- Corrigir problemas de layout ou responsividade
- Ajustar o design system
- Construir a sidebar, navbar pública ou hero

---

### QA Engineer — `qa.md`

**Especialidade:** Testes funcionais de UI com Playwright, validação de fluxos, design e segurança.

**Responsabilidades:**
- Verificar se os fluxos de usuário funcionam como esperado
- Validar o design em relação ao design system
- Testar segurança básica (isolamento de usuários, CSRF, redirects)
- Reportar falhas com passos de reprodução claros

**Ferramenta MCP:** `playwright` — para navegar e interagir com o sistema Django em execução.

**Quando usar:**
- Após implementar uma nova funcionalidade (backend + frontend prontos)
- Antes de considerar uma sprint concluída
- Para validar que um bug foi corrigido
- Para verificar consistência visual entre páginas

> **Pré-requisito para o agente QA:** o servidor Django deve estar rodando em `http://127.0.0.1:8000`.
> Execute: `source venv/bin/activate && python manage.py runserver`

---

## Como usar os agentes

Ao iniciar uma conversa com Claude Code para uma tarefa específica, instrua-o a atuar como o agente correspondente referenciando o arquivo:

```
Atue como o agente definido em agents/backend.md e implemente o model de Transação conforme descrito no PRD.
```

```
Atue como o agente definido em agents/frontend.md e crie o template de listagem de transações.
```

```
Atue como o agente definido em agents/qa.md e teste o módulo de autenticação com o servidor rodando.
```

---

## Stack do projeto

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Framework | Django 6.x |
| Frontend | Django Template Language |
| CSS | TailwindCSS via CDN |
| Fonte | Inter (Google Fonts) |
| Banco de dados | SQLite |
| Autenticação | Django Auth com EmailBackend customizado |
