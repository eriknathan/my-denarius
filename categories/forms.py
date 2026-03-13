from django import forms

from core.form_css import INPUT_CLASS

from .models import Category


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
