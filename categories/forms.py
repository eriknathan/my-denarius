from django import forms

from .models import Category

INPUT_CLASS = (
    'block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm '
    'text-gray-900 placeholder-gray-400 focus:border-emerald-500 '
    'focus:outline-none focus:ring-1 focus:ring-emerald-500'
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nome da categoria',
            }),
            'category_type': forms.Select(attrs={
                'class': INPUT_CLASS,
            }),
        }
