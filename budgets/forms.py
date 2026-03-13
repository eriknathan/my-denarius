import datetime
from django import forms

from categories.models import Category
from core.form_css import INPUT_CLASS

from .models import Budget


class BudgetForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(
                user=user, category_type='expense',
            )
        # Format existing month value for HTML month input
        if self.instance and self.instance.pk and self.instance.month:
            self.initial['month'] = self.instance.month.strftime('%Y-%m')

    def clean_month(self):
        raw = self.data.get('month', '')
        if raw and len(raw) == 7:
            try:
                year, month = raw.split('-')
                return datetime.date(int(year), int(month), 1)
            except (ValueError, TypeError):
                pass
        value = self.cleaned_data.get('month')
        if value:
            return value.replace(day=1)
        raise forms.ValidationError('Mês inválido.')

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASS}),
            'amount': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'step': '0.01',
                'min': '0.01',
            }),
            'month': forms.DateInput(attrs={
                'class': INPUT_CLASS,
                'type': 'month',
            }),
        }
