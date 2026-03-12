import datetime
import json
from decimal import Decimal
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone

import openai

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


def _decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')


def build_financial_context(user):
    today = timezone.localdate()

    accounts = Account.objects.filter(user=user).values('name', 'account_type', 'initial_balance')
    categories = Category.objects.filter(user=user).values('name', 'category_type')

    all_income = (
        Transaction.objects.filter(user=user, transaction_type='income')
        .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )
    all_expenses = (
        Transaction.objects.filter(user=user, transaction_type='expense')
        .aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )

    month_income = (
        Transaction.objects.filter(
            user=user, transaction_type='income',
            date__month=today.month, date__year=today.year,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )
    month_expenses = (
        Transaction.objects.filter(
            user=user, transaction_type='expense',
            date__month=today.month, date__year=today.year,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    )

    category_breakdown = (
        Transaction.objects
        .filter(
            user=user, transaction_type='expense',
            date__month=today.month, date__year=today.year,
            category__isnull=False,
        )
        .select_related('category')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    recent_transactions = (
        Transaction.objects
        .filter(user=user)
        .select_related('account', 'category')
        .values('description', 'amount', 'transaction_type', 'date', 'account__name', 'category__name')
        [:30]
    )

    largest_expense = (
        Transaction.objects
        .filter(
            user=user, transaction_type='expense',
            date__month=today.month, date__year=today.year,
        )
        .select_related('category')
        .order_by('-amount')
        .values('description', 'amount', 'category__name', 'date')
        .first()
    )

    return {
        'today': today.strftime('%d/%m/%Y'),
        'current_month': today.strftime('%B de %Y'),
        'accounts': list(accounts),
        'categories': list(categories),
        'summary': {
            'all_time_income': all_income,
            'all_time_expenses': all_expenses,
            'net_balance': all_income - all_expenses,
            'month_income': month_income,
            'month_expenses': month_expenses,
            'month_net': month_income - month_expenses,
        },
        'category_breakdown_this_month': list(category_breakdown),
        'recent_transactions': list(recent_transactions),
        'largest_expense_this_month': largest_expense,
    }


def build_system_prompt(financial_context):
    context_json = json.dumps(
        financial_context,
        ensure_ascii=False,
        default=_decimal_serializer,
    )

    return f"""Você é um assistente financeiro pessoal integrado ao sistema my-denarius.
Seu papel é responder perguntas sobre as finanças do usuário de forma clara, objetiva e em português brasileiro.

Regras:
- Responda sempre em português brasileiro
- Use os dados fornecidos abaixo para embasar suas respostas
- Valores monetários devem ser formatados como R$ X.XXX,XX
- Se a resposta não puder ser determinada pelos dados disponíveis, diga isso claramente
- Nunca invente dados ou faça suposições não embasadas nos dados
- Você tem acesso apenas a dados de leitura — não é possível criar, editar ou excluir registros
- Seja conciso: respostas curtas e diretas são preferíveis

Dados financeiros do usuário (em JSON):
{context_json}
"""


def ask_openai(user, question, conversation_history):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    financial_context = build_financial_context(user)
    system_prompt = build_system_prompt(financial_context)

    messages = [{'role': 'system', 'content': system_prompt}]
    messages.extend(conversation_history)
    messages.append({'role': 'user', 'content': question})

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content
