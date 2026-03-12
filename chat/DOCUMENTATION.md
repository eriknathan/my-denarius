# Chat de Ajuda — Documentação Técnica

## Visão Geral

O **Chat de Ajuda** é uma funcionalidade do my-denarius que permite ao usuário fazer perguntas em linguagem natural sobre suas finanças. O sistema consulta o banco de dados do Django em tempo real e utiliza a API da OpenAI para gerar respostas contextualizadas e precisas.

---

## Arquitetura da Integração

```
┌─────────────────────────────────────────────────────────────┐
│                        Navegador                            │
│                                                             │
│  [Input do usuário] ──fetch (POST JSON)──► /chat/mensagem/  │
│                                                             │
│  [Bolha de resposta] ◄── JSON { answer } ────────────────── │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Django (views.py)  │
                    │   ChatMessageView   │
                    │                     │
                    │  1. Lê sessão       │
                    │  2. Valida input    │
                    │  3. Chama services  │
                    └──────────┬──────────┘
                               │
              ┌────────────────▼─────────────────┐
              │         services.py               │
              │                                   │
              │  build_financial_context(user)    │
              │  ┌─────────────────────────────┐  │
              │  │  ORM queries (somente leitura)│ │
              │  │  - Account.objects.filter()  │  │
              │  │  - Category.objects.filter() │  │
              │  │  - Transaction.objects...    │  │
              │  └──────────────┬──────────────┘  │
              │                 │ dict com dados   │
              │  build_system_prompt(context)      │
              │                 │ string prompt    │
              │  ask_openai(user, question, hist)  │
              └─────────────────┬─────────────────┘
                                │
                   ┌────────────▼────────────┐
                   │      API OpenAI          │
                   │  POST /chat/completions  │
                   │  model: gpt-4.1-nano     │
                   │  (ou conforme .env)      │
                   └────────────┬────────────┘
                                │
                         { resposta em texto }
```

---

## Nota sobre MCP (Model Context Protocol)

Esta implementação **não utiliza um servidor MCP externo**. O termo "MCP" aqui se refere ao padrão conceitual de fornecer contexto ao modelo — o Django atua como a "ponte de contexto" entre o banco de dados e a OpenAI:

- Em vez de um servidor MCP separado consultando o banco via ferramentas externas, a função `build_financial_context()` em `services.py` executa diretamente as queries ORM e serializa os dados como JSON
- Esse JSON é embutido no `system prompt` enviado à OpenAI a cada requisição
- O modelo recebe os dados estruturados e os usa para responder à pergunta do usuário

Essa abordagem é equivalente ao padrão MCP de "injeção de contexto", porém totalmente contida no Django, sem dependências externas além da `openai` SDK.

---

## Fluxo Detalhado de uma Mensagem

### 1. Frontend envia a pergunta

O template `templates/chat/index.html` intercepta o `submit` do formulário com JavaScript e faz uma requisição assíncrona:

```js
fetch('/chat/mensagem/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,       // proteção CSRF via header
  },
  body: JSON.stringify({ question }),
})
```

### 2. Django valida e processa (`views.py`)

`ChatMessageView.post()` realiza:

1. Parse do JSON do body (`request.body`)
2. Validação: pergunta não vazia, máximo de 500 caracteres
3. Recupera o histórico da sessão: `request.session.get('chat_history', [])`
4. Chama `ask_openai(request.user, question, history)` — o `request.user` garante isolamento de dados
5. Appenda a nova troca ao histórico da sessão
6. Limita o histórico a 20 pares (40 mensagens) para controle de tokens
7. Retorna `JsonResponse({'answer': resposta})`

### 3. Construção do contexto financeiro (`services.py`)

`build_financial_context(user)` executa as seguintes queries, **sempre filtradas por `user`**:

| Dado | Query | Finalidade |
|---|---|---|
| Contas | `Account.objects.filter(user=user)` | Nome, tipo e saldo inicial |
| Categorias | `Category.objects.filter(user=user)` | Nome e tipo (receita/despesa) |
| Receita total | `Transaction.filter(type='income').aggregate(Sum)` | Visão geral |
| Despesa total | `Transaction.filter(type='expense').aggregate(Sum)` | Visão geral |
| Receita do mês | filtro por mês/ano atual | Resumo mensal |
| Despesa do mês | filtro por mês/ano atual | Resumo mensal |
| Breakdown por categoria | GROUP BY categoria, mês atual | Perguntas como "gastei mais em quê?" |
| Últimas 30 transações | `.order_by('-date')[:30]` | Perguntas sobre transações recentes |
| Maior despesa do mês | `.order_by('-amount').first()` | "Qual foi meu maior gasto?" |

O resultado é um `dict` Python serializado para JSON com um encoder customizado que trata `Decimal` (converte para `float`) e `datetime.date` (converte para ISO 8601).

### 4. System prompt enviado à OpenAI

O JSON do contexto financeiro é embutido diretamente no `system prompt`:

```
Você é um assistente financeiro pessoal integrado ao sistema my-denarius.
...regras de comportamento...

Dados financeiros do usuário (em JSON):
{ "today": "12/03/2026", "accounts": [...], "summary": {...}, ... }
```

### 5. Chamada à API OpenAI

A lista de mensagens enviada para `chat.completions.create` tem a estrutura:

```python
[
  { "role": "system",    "content": "<system_prompt_com_dados_financeiros>" },
  { "role": "user",      "content": "<pergunta anterior 1>" },   # histórico
  { "role": "assistant", "content": "<resposta anterior 1>" },   # histórico
  ...
  { "role": "user",      "content": "<pergunta atual>" },
]
```

O contexto financeiro é **reconstruído a cada requisição** — os dados são sempre frescos, refletindo o estado atual do banco.

---

## Segurança e Isolamento de Dados

- Todas as views exigem autenticação via `LoginRequiredMixin` — requisições não autenticadas são redirecionadas para `/login/`
- Todas as queries em `build_financial_context()` filtram obrigatoriamente por `user` — é impossível acessar dados de outro usuário
- A `OPENAI_API_KEY` é carregada exclusivamente via variável de ambiente (`.env`) e nunca aparece no código-fonte
- O chat é **somente leitura**: nenhuma view ou serviço executa operações de escrita no banco
- A proteção CSRF é mantida via header `X-CSRFToken` nas requisições AJAX — nenhuma view usa `@csrf_exempt`

---

## Histórico de Conversa (Sessão)

O histórico é armazenado na sessão Django sob a chave `chat_history`:

```python
SESSION_KEY = 'chat_history'   # chave na sessão
MAX_HISTORY = 20               # máximo de pares pergunta/resposta
```

- Formato: lista de dicts `[{"role": "user"|"assistant", "content": "..."}]`
- Esse formato é idêntico ao esperado pela API OpenAI, sem transformações
- O histórico é passado integralmente a cada nova requisição, dando ao modelo memória da conversa
- Ao atingir 20 pares (40 mensagens), as mais antigas são descartadas
- O usuário pode limpar o histórico via botão "Limpar conversa" (endpoint `POST /chat/limpar/`)
- O histórico **não é persistido no banco de dados** — é perdido ao expirar a sessão

---

## Configuração

### Variáveis de ambiente (`.env`)

```env
OPENAI_API_KEY=sk-...       # obrigatório
OPENAI_MODEL=gpt-4.1-nano   # opcional, padrão: gpt-4o-mini
```

### Settings Django (`core/settings.py`)

```python
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_MODEL   = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
```

---

## Estrutura de Arquivos

```
chat/
├── __init__.py
├── apps.py            # ChatConfig
├── urls.py            # 3 endpoints: index, mensagem, limpar
├── views.py           # ChatView, ChatMessageView, ChatClearView
├── services.py        # build_financial_context, build_system_prompt, ask_openai
└── DOCUMENTATION.md   # este arquivo

templates/
└── chat/
    └── index.html     # interface do chat
```

### URLs registradas

| Método | URL | View | Descrição |
|---|---|---|---|
| GET | `/chat/` | `ChatView` | Renderiza a página do chat |
| POST | `/chat/mensagem/` | `ChatMessageView` | Processa uma pergunta, retorna JSON |
| POST | `/chat/limpar/` | `ChatClearView` | Limpa o histórico da sessão |

---

## Estimativa de Tokens por Requisição

| Componente | Tokens aproximados |
|---|---|
| System prompt (texto fixo) | ~200 |
| Contexto financeiro (JSON) | ~600–1.200 |
| Histórico da conversa (20 pares) | ~2.000–4.000 |
| Pergunta do usuário | ~20–100 |
| **Total (input)** | **~3.000–5.500** |
| Resposta (max_tokens) | até 800 |

Com `gpt-4.1-nano`, o custo por conversa é muito baixo. O parâmetro `temperature=0.3` foi escolhido para respostas factuais e consistentes.
