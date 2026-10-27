from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='Password123!',
            first_name='John',
            last_name='Doe'
        )

    def test_user_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_email_rejected(self):
        response = self.client.post(reverse('register'), {
            'username': 'unique_user',
            'first_name': 'Another',
            'last_name': 'Person',
            'email': 'john@example.com', # duplicate
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email already exists.")

    def test_user_login_and_logout(self):
        # Login
        login_resp = self.client.post(reverse('login'), {
            'username': 'johndoe',
            'password': 'Password123!'
        })
        self.assertEqual(login_resp.status_code, 302)
        # Dashboard is accessible
        dash_resp = self.client.get(reverse('dashboard'))
        self.assertEqual(dash_resp.status_code, 200)
        self.assertContains(dash_resp, "John")

        # Logout
        logout_resp = self.client.post(reverse('logout'))
        self.assertEqual(logout_resp.status_code, 302)
        # Dashboard redirects to login
        dash_unauth = self.client.get(reverse('dashboard'))
        self.assertEqual(dash_unauth.status_code, 302)

    def test_unauthenticated_access_protection(self):
        response = self.client.get(reverse('profile_detail'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
