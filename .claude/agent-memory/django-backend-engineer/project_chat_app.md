---
name: chat app architecture
description: Chat de Ajuda app — OpenAI-powered financial assistant wired to user's transaction data
type: project
---

The `chat` app provides an AI-powered financial assistant ("Chat de Ajuda") for authenticated users.

**Why:** Lets users ask natural-language questions about their finances; responses are grounded in real ORM data from accounts, categories, and transactions.

**How to apply:** When adding AI/chat features, extend this app. Do not add model-level storage — conversation history lives in the Django session under the key `chat_history`.

Key design decisions:
- No database model: history stored in `request.session['chat_history']` (max 20 turns × 2 = 40 messages)
- `chat/services.py` contains all OpenAI logic: `build_financial_context(user)`, `build_system_prompt(context)`, `ask_openai(user, question, history)`
- Financial context snapshot built fresh on every request (no caching)
- Three views: `ChatView` (TemplateView, GET), `ChatMessageView` (View, POST → JSON), `ChatClearView` (View, POST → JSON)
- URL prefix: `chat/` with namespace `chat`; routes: `''` (index), `mensagem/` (message), `limpar/` (clear)
- Settings added: `OPENAI_API_KEY` and `OPENAI_MODEL` read from `.env` via `python-dotenv`; default model `gpt-4o-mini`
- `python-dotenv` and `openai>=1.0.0` added to `requirements.txt`
- `load_dotenv(BASE_DIR / '.env')` called in `core/settings.py` after `BASE_DIR` is defined
