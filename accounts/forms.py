from django import forms

from core.form_css import INPUT_CLASS, NUMBER_CLASS

from .models import Account


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
