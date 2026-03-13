import datetime

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Account
from categories.models import Category

from .models import Transaction

User = get_user_model()


def _create_user(email='user@example.com', password='senha123'):
    return User.objects.create_user(
        email=email,
        password=password,
        first_name='Test',
        last_name='User',
    )


def _create_account(user, name='Conta'):
    return Account.objects.create(
        user=user,
        name=name,
        account_type='checking',
        initial_balance='0.00',
    )


def _create_category(user, name='Categoria', category_type='expense'):
    return Category.objects.create(
        user=user,
        name=name,
        category_type=category_type,
    )


def _create_transaction(user, account, category=None, **kwargs):
    defaults = {
        'description': 'Transação teste',
        'amount': '100.00',
        'transaction_type': 'expense',
        'date': datetime.date.today(),
        'is_recurring': False,
    }
    defaults.update(kwargs)
    return Transaction.objects.create(
        user=user,
        account=account,
        category=category,
        **defaults,
    )


class TransactionModelTest(TestCase):
    def test_str_returns_description_and_amount(self):
        user = _create_user()
        account = _create_account(user)
        transaction = _create_transaction(user, account, description='Aluguel', amount='1500.00')
        self.assertIn('Aluguel', str(transaction))
        self.assertIn('1500.00', str(transaction))

    def test_timestamps_are_set(self):
        user = _create_user()
        account = _create_account(user)
        transaction = _create_transaction(user, account)
        self.assertIsNotNone(transaction.created_at)
        self.assertIsNotNone(transaction.updated_at)


class TransactionOwnershipTest(TestCase):
    def setUp(self):
        self.user_a = _create_user('a@example.com')
        self.user_b = _create_user('b@example.com')
        self.account_a = _create_account(self.user_a, 'Conta A')
        self.account_b = _create_account(self.user_b, 'Conta B')
        self.transaction_a = _create_transaction(self.user_a, self.account_a)
        self.transaction_b = _create_transaction(self.user_b, self.account_b)

    def test_list_shows_only_own_transactions(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 200)
        transactions = list(response.context['transactions'])
        self.assertIn(self.transaction_a, transactions)
        self.assertNotIn(self.transaction_b, transactions)

    def test_user_a_cannot_edit_user_b_transaction(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('transactions:update', kwargs={'pk': self.transaction_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_delete_user_b_transaction(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('transactions:delete', kwargs={'pk': self.transaction_b.pk})
        )
        self.assertEqual(response.status_code, 404)


class TransactionListFilterTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.force_login(self.user)
        self.account = _create_account(self.user)
        self.income_tx = _create_transaction(
            self.user, self.account,
            description='Salário',
            transaction_type='income',
            date=datetime.date(2026, 1, 15),
        )
        self.expense_tx = _create_transaction(
            self.user, self.account,
            description='Aluguel',
            transaction_type='expense',
            date=datetime.date(2026, 2, 10),
        )

    def test_filter_by_transaction_type_income(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'transaction_type': 'income'},
        )
        self.assertEqual(response.status_code, 200)
        transactions = list(response.context['transactions'])
        self.assertIn(self.income_tx, transactions)
        self.assertNotIn(self.expense_tx, transactions)

    def test_filter_by_transaction_type_expense(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'transaction_type': 'expense'},
        )
        transactions = list(response.context['transactions'])
        self.assertNotIn(self.income_tx, transactions)
        self.assertIn(self.expense_tx, transactions)

    def test_filter_by_date_start(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'date_start': '2026-02-01'},
        )
        transactions = list(response.context['transactions'])
        self.assertIn(self.expense_tx, transactions)
        self.assertNotIn(self.income_tx, transactions)

    def test_filter_by_date_end(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'date_end': '2026-01-31'},
        )
        transactions = list(response.context['transactions'])
        self.assertIn(self.income_tx, transactions)
        self.assertNotIn(self.expense_tx, transactions)

    def test_filter_by_date_range(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'date_start': '2026-01-01', 'date_end': '2026-01-31'},
        )
        transactions = list(response.context['transactions'])
        self.assertIn(self.income_tx, transactions)
        self.assertNotIn(self.expense_tx, transactions)


class TransactionCRUDTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.force_login(self.user)
        self.account = _create_account(self.user)
        self.category = _create_category(self.user)

    def test_unauthenticated_list_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('transactions:list'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('transactions:list')}",
        )

    def test_create_transaction(self):
        response = self.client.post(reverse('transactions:create'), {
            'description': 'Conta de Luz',
            'amount': '150.00',
            'transaction_type': 'expense',
            'date': '2026-03-01',
            'account': self.account.pk,
            'category': self.category.pk,
            'notes': '',
            'is_recurring': False,
        })
        self.assertRedirects(response, reverse('transactions:list'))
        self.assertTrue(Transaction.objects.filter(
            user=self.user, description='Conta de Luz',
        ).exists())

    def test_delete_transaction(self):
        transaction = _create_transaction(self.user, self.account)
        response = self.client.post(
            reverse('transactions:delete', kwargs={'pk': transaction.pk})
        )
        self.assertRedirects(response, reverse('transactions:list'))
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())


class GenerateRecurringCommandTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.account = _create_account(self.user)
        self.category = _create_category(self.user)
        today = timezone.localdate()
        self.template_tx = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            description='Assinatura Mensal',
            amount='49.90',
            transaction_type='expense',
            date=datetime.date(today.year, today.month, 1),
            is_recurring=True,
            recurrence_day=today.day,
        )

    def test_command_creates_transaction_for_current_month(self):
        call_command('generate_recurring', verbosity=0)
        today = timezone.localdate()
        self.assertTrue(Transaction.objects.filter(
            user=self.user,
            description='Assinatura Mensal',
            date__year=today.year,
            date__month=today.month,
            is_recurring=False,
        ).exists())

    def test_command_is_idempotent(self):
        call_command('generate_recurring', verbosity=0)
        call_command('generate_recurring', verbosity=0)
        today = timezone.localdate()
        count = Transaction.objects.filter(
            user=self.user,
            description='Assinatura Mensal',
            date__year=today.year,
            date__month=today.month,
            is_recurring=False,
        ).count()
        self.assertEqual(count, 1)
