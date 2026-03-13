from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Category

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


class CategoryModelTest(TestCase):
    def test_str_includes_name_and_type_display(self):
        user = _create_user()
        category = _create_category(user, 'Salário', 'income')
        self.assertEqual(str(category), 'Salário (Receita)')

    def test_expense_category_str(self):
        user = _create_user()
        category = _create_category(user, 'Mercado', 'expense')
        self.assertEqual(str(category), 'Mercado (Despesa)')

    def test_timestamps_are_set(self):
        user = _create_user()
        category = _create_category(user)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)

    def test_category_type_choices(self):
        user = _create_user()
        income_cat = _create_category(user, 'Renda', 'income')
        expense_cat = _create_category(user, 'Gasto', 'expense')
        self.assertEqual(income_cat.category_type, 'income')
        self.assertEqual(expense_cat.category_type, 'expense')


class CategoryOwnershipTest(TestCase):
    def setUp(self):
        self.user_a = _create_user('a@example.com')
        self.user_b = _create_user('b@example.com')
        self.category_a = _create_category(self.user_a, 'Cat A')
        self.category_b = _create_category(self.user_b, 'Cat B')

    def test_list_shows_only_own_categories(self):
        self.client.force_login(self.user_a)
        response = self.client.get(reverse('categories:list'))
        self.assertEqual(response.status_code, 200)
        categories = list(response.context['categories'])
        self.assertIn(self.category_a, categories)
        self.assertNotIn(self.category_b, categories)

    def test_user_a_cannot_edit_user_b_category(self):
        self.client.force_login(self.user_a)
        response = self.client.get(
            reverse('categories:update', kwargs={'pk': self.category_b.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_user_a_cannot_delete_user_b_category(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse('categories:delete', kwargs={'pk': self.category_b.pk})
        )
        self.assertEqual(response.status_code, 404)


class CategoryCRUDTest(TestCase):
    def setUp(self):
        self.user = _create_user()
        self.client.force_login(self.user)

    def test_unauthenticated_list_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('categories:list'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('categories:list')}",
        )

    def test_create_income_category(self):
        response = self.client.post(reverse('categories:create'), {
            'name': 'Freelance',
            'category_type': 'income',
        })
        self.assertRedirects(response, reverse('categories:list'))
        self.assertTrue(Category.objects.filter(
            user=self.user, name='Freelance', category_type='income',
        ).exists())

    def test_create_expense_category(self):
        response = self.client.post(reverse('categories:create'), {
            'name': 'Aluguel',
            'category_type': 'expense',
        })
        self.assertRedirects(response, reverse('categories:list'))
        self.assertTrue(Category.objects.filter(
            user=self.user, name='Aluguel', category_type='expense',
        ).exists())

    def test_update_category(self):
        category = _create_category(self.user, 'Antes')
        response = self.client.post(
            reverse('categories:update', kwargs={'pk': category.pk}),
            {
                'name': 'Depois',
                'category_type': 'income',
            },
        )
        self.assertRedirects(response, reverse('categories:list'))
        category.refresh_from_db()
        self.assertEqual(category.name, 'Depois')
        self.assertEqual(category.category_type, 'income')

    def test_delete_category(self):
        category = _create_category(self.user, 'Para Excluir')
        response = self.client.post(
            reverse('categories:delete', kwargs={'pk': category.pk})
        )
        self.assertRedirects(response, reverse('categories:list'))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())
