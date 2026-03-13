from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Account

User = get_user_model()


def _create_user(email='user@example.com', password='senha123'):
    return User.objects.create_user(
        email=email,
        password=password,
        first_name='Test',
        last_name='User',
    )


def _create_account(user, name='Conta Corrente', account_type='checking'):
    return Account.objects.create(
        user=user,
        name=name,
        account_type=account_type,
        initial_balance=Decimal('100.00'),
    )


class AccountModelTest(TestCase):
    def test_str_returns_name(self):
        user = _create_user()
        account = _create_account(user)
        self.assertEqual(str(account), 'Conta Corrente')

    def test_current_balance_with_no_transactions(self):
        user = _create_user()
        account = _create_account(user)
        self.assertEqual(account.current_balance, Decimal('100.00'))

    def test_timestamps_are_set(self):
        user = _create_user()
        account = _create_account(user)
        self.assertIsNotNone(account.created_at)
        self.assertIsNotNone(account.updated_at)


class AccountOwnershipTest(TestCase):
    def setUp(self):
        self.user_a = _create_user('a@example.com')
        self.user_b = _create_user('b@example.com')
        self.account_a = _create_account(self.user_a, 'Conta A')
        self.account_b = _create_account(self.user_b, 'Conta B')

    def test_list_shows_only_own_accounts(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)
        accounts = list(response.context['accounts'])
        self.assertIn(self.account_a, accounts)
        self.assertNotIn(self.account_b, accounts)

    def test_user_a_cannot_edit_user_b_account(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('accounts:update', kwargs={'pk': self.account_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_delete_user_b_account(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('accounts:delete', kwargs={'pk': self.account_b.pk})
        )
        self.assertEqual(response.status_code, 404)


class AccountCRUDTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.force_login(self.user)

    def test_unauthenticated_list_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:list'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('accounts:list')}",
        )

    def test_create_account(self):
        response = self.client.post(reverse('accounts:create'), {
            'name': 'Nova Conta',
            'account_type': 'savings',
            'initial_balance': '500.00',
        })
        self.assertRedirects(response, reverse('accounts:list'))
        self.assertTrue(Account.objects.filter(
            user=self.user, name='Nova Conta',
        ).exists())

    def test_update_account(self):
        account = _create_account(self.user, 'Antes')
        response = self.client.post(
            reverse('accounts:update', kwargs={'pk': account.pk}),
            {
                'name': 'Depois',
                'account_type': 'checking',
                'initial_balance': '200.00',
            },
        )
        self.assertRedirects(response, reverse('accounts:list'))
        account.refresh_from_db()
        self.assertEqual(account.name, 'Depois')

    def test_delete_account(self):
        account = _create_account(self.user, 'Para Excluir')
        response = self.client.post(
            reverse('accounts:delete', kwargs={'pk': account.pk})
        )
        self.assertRedirects(response, reverse('accounts:list'))
        self.assertFalse(Account.objects.filter(pk=account.pk).exists())
