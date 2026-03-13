from django import forms

from accounts.models import Account
from categories.models import Category
from core.form_css import INPUT_CLASS, NUMBER_CLASS, TEXTAREA_CLASS

from .models import Transaction


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Transaction
        fields = [
            'description',
            'amount',
            'transaction_type',
            'date',
            'account',
            'category',
            'notes',
            'is_recurring',
            'recurrence_day',
        ]
        widgets = {
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Descrição da transação',
            }),
            'amount': forms.NumberInput(attrs={
                'class': NUMBER_CLASS,
                'step': '0.01',
                'min': '0.01',
            }),
            'transaction_type': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
            'date': forms.DateInput(attrs={
                'class': INPUT_CLASS,
                'type': 'date',
            }),
            'account': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
            'notes': forms.Textarea(attrs={
                'class': TEXTAREA_CLASS,
                'rows': 3,
                'placeholder': 'Observações (opcional)',
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500',
                'id': 'id_is_recurring',
            }),
            'recurrence_day': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': '1',
                'max': '31',
                'placeholder': 'Dia (1-31)',
            }),
        }
