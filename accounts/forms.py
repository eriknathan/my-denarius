from django import forms

from .models import Account

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


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'initial_balance']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nome da conta',
            }),
            'account_type': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
            'initial_balance': forms.NumberInput(attrs={
                'class': NUMBER_CLASS,
                'step': '0.01',
            }),
        }
