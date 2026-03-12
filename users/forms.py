from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

INPUT_CSS = (
    'block w-full px-3 py-2 border border-gray-300 rounded-lg '
    'text-sm text-gray-800 placeholder-gray-400 '
    'focus:outline-none focus:ring-2 focus:ring-emerald-500 '
    'focus:border-emerald-500 transition-colors duration-200'
)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Nome',
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'Sobrenome',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CSS,
                'placeholder': 'seu@email.com',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': INPUT_CSS,
            'placeholder': 'Senha',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': INPUT_CSS,
            'placeholder': 'Confirme a senha',
        })


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': INPUT_CSS,
            'placeholder': 'seu@email.com',
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CSS,
            'placeholder': 'Senha',
        }),
    )
