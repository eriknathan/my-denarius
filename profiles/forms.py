from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

INPUT_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder-gray-400 focus:border-emerald-500 '
    'focus:outline-none focus:ring-1 focus:ring-emerald-500'
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Telefone',
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nome',
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Sobrenome',
            }),
        }
