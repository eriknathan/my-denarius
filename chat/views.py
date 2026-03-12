import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from .services import ask_openai

SESSION_KEY = 'chat_history'
MAX_HISTORY = 20

SUGGESTED_QUESTIONS = [
    'Qual foi meu maior gasto esse mês?',
    'Quanto gastei com alimentação esse mês?',
    'Qual é meu saldo atual?',
    'Quais são minhas receitas desse mês?',
    'Em qual categoria gastei mais?',
    'Como estão minhas finanças esse mês?',
]


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.request.session.get(SESSION_KEY, [])
        context['suggestions'] = SUGGESTED_QUESTIONS
        return context


class ChatMessageView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            question = body.get('question', '').strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Requisição inválida.'}, status=400)

        if not question:
            return JsonResponse({'error': 'A pergunta não pode ser vazia.'}, status=400)

        if len(question) > 500:
            return JsonResponse(
                {'error': 'Pergunta muito longa. Máximo 500 caracteres.'}, status=400
            )

        history = request.session.get(SESSION_KEY, [])

        try:
            answer = ask_openai(request.user, question, history)
        except Exception as exc:
            return JsonResponse(
                {'error': f'Erro ao consultar o assistente: {str(exc)}'}, status=500
            )

        history.append({'role': 'user', 'content': question})
        history.append({'role': 'assistant', 'content': answer})

        if len(history) > MAX_HISTORY * 2:
            history = history[-(MAX_HISTORY * 2):]

        request.session[SESSION_KEY] = history
        request.session.modified = True

        return JsonResponse({'answer': answer})


class ChatClearView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        request.session.pop(SESSION_KEY, None)
        return JsonResponse({'ok': True})
