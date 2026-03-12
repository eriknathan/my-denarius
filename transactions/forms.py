from django import forms

from accounts.models import Account
from categories.models import Category

from .models import Transaction

INPUT_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder-gray-400 focus:border-emerald-500 '
    'focus:outline-none focus:ring-1 focus:ring-emerald-500'
)
NUMBER_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 focus:border-emerald-500 focus:outline-none '
    'focus:ring-1 focus:ring-emerald-500'
)
TEXTAREA_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder-gray-400 resize-none focus:border-emerald-500 '
    'focus:outline-none focus:ring-1 focus:ring-emerald-500'
)


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
        }
