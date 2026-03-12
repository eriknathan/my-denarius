# Modelos de Dados

## Diagrama de relacionamentos (ERD)

```
USER ──────────── PROFILE        (1:1)
USER ──────────── ACCOUNT         (1:N)
USER ──────────── CATEGORY        (1:N)
USER ──────────── TRANSACTION     (1:N)
ACCOUNT ────────── TRANSACTION    (1:N)
CATEGORY ───────── TRANSACTION    (1:N, nullable)
```

---

## User

App: `users` | Model: `User` (herda de `AbstractUser`)

| Campo | Tipo | Detalhes |
|---|---|---|
| `id` | AutoField | PK |
| `email` | EmailField | único, `USERNAME_FIELD` |
| `first_name` | CharField | obrigatório |
| `last_name` | CharField | obrigatório |
| `password` | CharField | gerenciado pelo Django |
| `is_active` | BooleanField | padrão `True` |
| `date_joined` | DateTimeField | auto |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

Observações:
- `username = None` — campo removido
- `USERNAME_FIELD = 'email'`
- `REQUIRED_FIELDS = ['first_name', 'last_name']`
- `AUTH_USER_MODEL = 'users.User'` em `settings.py`

---

## Profile

App: `profiles` | Model: `Profile`

| Campo | Tipo | Detalhes |
|---|---|---|
| `id` | AutoField | PK |
| `user` | OneToOneField → User | `on_delete=CASCADE` |
| `phone` | CharField(20) | `blank=True` |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

Observações:
- Criado automaticamente via signal `post_save` no model `User`
- Acessado via `request.user.profile`

---

## Account

App: `accounts` | Model: `Account`

| Campo | Tipo | Detalhes |
|---|---|---|
| `id` | AutoField | PK |
| `user` | ForeignKey → User | `on_delete=CASCADE` |
| `name` | CharField(100) | nome da conta |
| `account_type` | CharField(20) | choices: `checking`, `savings`, `cash`, `other` |
| `initial_balance` | DecimalField(12,2) | `default=0` |
| `current_balance` | DecimalField(12,2) | calculado a partir das transações |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

Choices de `account_type`:

| Valor | Label |
|---|---|
| `checking` | Corrente |
| `savings` | Poupança |
| `cash` | Dinheiro |
| `other` | Outro |

---

## Category

App: `categories` | Model: `Category`

| Campo | Tipo | Detalhes |
|---|---|---|
| `id` | AutoField | PK |
| `user` | ForeignKey → User | `on_delete=CASCADE` |
| `name` | CharField(100) | nome da categoria |
| `category_type` | CharField(10) | choices: `income`, `expense` |
| `color` | CharField(7) | hex opcional, ex: `#059669` |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

Choices de `category_type`:

| Valor | Label |
|---|---|
| `income` | Receita |
| `expense` | Despesa |

---

## Transaction

App: `transactions` | Model: `Transaction`

| Campo | Tipo | Detalhes |
|---|---|---|
| `id` | AutoField | PK |
| `user` | ForeignKey → User | `on_delete=CASCADE` |
| `account` | ForeignKey → Account | `on_delete=CASCADE` |
| `category` | ForeignKey → Category | `on_delete=SET_NULL`, `null=True`, `blank=True` |
| `description` | CharField(200) | — |
| `amount` | DecimalField(12,2) | sempre positivo |
| `transaction_type` | CharField(10) | choices: `income`, `expense` |
| `date` | DateField | data da transação |
| `notes` | TextField | `blank=True` |
| `created_at` | DateTimeField | `auto_now_add=True` |
| `updated_at` | DateTimeField | `auto_now=True` |

Choices de `transaction_type`:

| Valor | Label |
|---|---|
| `income` | Receita |
| `expense` | Despesa |

Observações:
- `class Meta: ordering = ['-date', '-created_at']`
- O campo `amount` é sempre positivo — o tipo (`income`/`expense`) define o sinal
- Ao criar ou editar uma transação, o `current_balance` da conta associada deve ser recalculado
