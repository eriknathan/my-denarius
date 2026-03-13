import datetime

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from categories.models import Category

from .forms import BudgetForm
from .models import Budget

User = get_user_model()


def _create_user(email='user@example.com', password='senha123'):
    return User.objects.create_user(
        email=email,
        password=password,
        first_name='Test',
        last_name='User',
    )


def _create_category(user, name='Alimentação', category_type='expense'):
    return Category.objects.create(
        user=user,
        name=name,
        category_type=category_type,
    )


def _create_budget(user, category, month=None, amount='500.00'):
    if month is None:
        month = datetime.date(2026, 3, 1)
    return Budget.objects.create(
        user=user,
        category=category,
        amount=amount,
        month=month,
    )


class BudgetModelTest(TestCase):
    def test_str_includes_category_month_and_amount(self):
        user = _create_user()
        category = _create_category(user, 'Supermercado')
        budget = _create_budget(user, category, datetime.date(2026, 3, 1), '300.00')
        result = str(budget)
        self.assertIn('Supermercado', result)
        self.assertIn('03/2026', result)
        self.assertIn('300.00', result)

    def test_timestamps_are_set(self):
        user = _create_user()
        category = _create_category(user)
        budget = _create_budget(user, category)
        self.assertIsNotNone(budget.created_at)
        self.assertIsNotNone(budget.updated_at)

    def test_unique_together_user_category_month(self):
        user = _create_user()
        category = _create_category(user)
        _create_budget(user, category, datetime.date(2026, 3, 1))
        with self.assertRaises(IntegrityError):
            Budget.objects.create(
                user=user,
                category=category,
                amount='999.00',
                month=datetime.date(2026, 3, 1),
            )

    def test_different_months_allowed_for_same_user_category(self):
        user = _create_user()
        category = _create_category(user)
        _create_budget(user, category, datetime.date(2026, 3, 1))
        budget_april = _create_budget(user, category, datetime.date(2026, 4, 1))
        self.assertIsNotNone(budget_april.pk)


class BudgetOwnershipTest(TestCase):
    def setUp(self):
        self.user_a = _create_user('a@example.com')
        self.user_b = _create_user('b@example.com')
        self.category_a = _create_category(self.user_a, 'Cat A')
        self.category_b = _create_category(self.user_b, 'Cat B')
        self.budget_a = _create_budget(self.user_a, self.category_a)
        self.budget_b = _create_budget(self.user_b, self.category_b)

    def test_list_shows_only_own_budgets(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('budgets:list'))
        self.assertEqual(response.status_code, 200)
        budgets_in_context = [
            item['budget'] for item in response.context['enriched']
        ]
        self.assertIn(self.budget_a, budgets_in_context)
        self.assertNotIn(self.budget_b, budgets_in_context)

    def test_user_a_cannot_edit_user_b_budget(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('budgets:update', kwargs={'pk': self.budget_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_delete_user_b_budget(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('budgets:delete', kwargs={'pk': self.budget_b.pk})
        )
        self.assertEqual(response.status_code, 404)


class BudgetCRUDTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.force_login(self.user)
        self.category = _create_category(self.user)

    def test_unauthenticated_list_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('budgets:list'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('budgets:list')}",
        )

    def test_create_budget(self):
        response = self.client.post(reverse('budgets:create'), {
            'category': self.category.pk,
            'amount': '800.00',
            'month': '2026-05-01',
        })
        self.assertRedirects(response, reverse('budgets:list'))
        self.assertTrue(Budget.objects.filter(
            user=self.user,
            category=self.category,
            month=datetime.date(2026, 5, 1),
        ).exists())

    def test_delete_budget(self):
        budget = _create_budget(self.user, self.category)
        response = self.client.post(
            reverse('budgets:delete', kwargs={'pk': budget.pk})
        )
        self.assertRedirects(response, reverse('budgets:list'))
        self.assertFalse(Budget.objects.filter(pk=budget.pk).exists())


class BudgetFormTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.category = _create_category(self.user)

    def test_clean_month_normalizes_mid_month_date_to_first(self):
        # Input with day != 1 must be normalized to the 1st of that month
        form = BudgetForm(
            data={
                'category': self.category.pk,
                'amount': '500.00',
                'month': '2026-03-15',
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['month'], datetime.date(2026, 3, 1))

    def test_clean_month_normalizes_end_of_month_to_first(self):
        form = BudgetForm(
            data={
                'category': self.category.pk,
                'amount': '200.00',
                'month': '2026-11-30',
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['month'], datetime.date(2026, 11, 1))

    def test_form_only_shows_expense_categories_for_user(self):
        income_category = _create_category(self.user, 'Salário', 'income')
        form = BudgetForm(user=self.user)
        queryset = form.fields['category'].queryset
        self.assertNotIn(income_category, queryset)
        self.assertIn(self.category, queryset)
