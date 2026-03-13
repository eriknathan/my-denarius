from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='senha123',
            first_name='Test',
            last_name='User',
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertIsNone(user.username)
        self.assertTrue(user.check_password('senha123'))

    def test_str_returns_email(self):
        user = User.objects.create_user(
            email='str@example.com',
            password='senha123',
            first_name='A',
            last_name='B',
        )
        self.assertEqual(str(user), 'str@example.com')

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='senha123')

    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_timestamps_are_set(self):
        user = User.objects.create_user(
            email='ts@example.com',
            password='senha123',
            first_name='T',
            last_name='S',
        )
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)


class RegisterViewTest(TestCase):
    def _create_user(self, email='existing@example.com', password='senha123'):
        return User.objects.create_user(
            email=email,
            password=password,
            first_name='Existing',
            last_name='User',
        )

    def test_register_page_loads(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_redirects_authenticated_user(self):
        user = self._create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('users:register'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_creates_user_and_redirects_to_dashboard(self):
        data = {
            'email': 'novo@example.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(email='novo@example.com').exists())


class LoginViewTest(TestCase):
    def _create_user(self, email='login@example.com', password='senha123'):
        return User.objects.create_user(
            email=email,
            password=password,
            first_name='Login',
            last_name='User',
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        self._create_user()
        response = self.client.post(reverse('users:login'), {
            'email': 'login@example.com',
            'password': 'senha123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_with_invalid_credentials(self):
        self._create_user()
        response = self.client.post(reverse('users:login'), {
            'email': 'login@example.com',
            'password': 'senhaerrada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail ou senha inválidos.')

    def test_login_redirects_authenticated_user(self):
        user = self._create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('users:login'))
        self.assertRedirects(response, reverse('dashboard'))
