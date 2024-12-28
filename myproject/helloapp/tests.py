from django.test import TestCase
from django.urls import reverse
from .models import BuddyMatchingUser
from .forms import BuddyMatchingUserCreationForm, LoginForm

class ModelsTestCase(TestCase):
    def test_buddy_matching_user_creation(self):
        user = BuddyMatchingUser.objects.create_user(
            email='john.doe@example.com',
            password='password123!',
            role='Buddy',
            first_name='John',
            surname='Doe'
        )
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertTrue(user.check_password('password123!'))

class FormsTestCase(TestCase):

    def test_buddy_matching_user_creation_form_valid(self):
        form_data = {
            'email': 'valid@example.com',
            'password1': 'password123!',
            'password2': 'password123!',
            'first_name': 'Valid',
            'surname': 'User',
            'role': 'Buddy',
            'preferred_language': 'German',
            'degree_level': 'Bachelors', 
            'app_matr_number': '12345', 
            'department': 'FB 1', 
            'country': 'randomCountry', 
            'preferred_number_of_partners': '2', 
            'is_permitted': 'true'
        }
        form = BuddyMatchingUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_buddy_matching_user_creation_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email',
            'password1': 'password123!',
            'password2': 'password123!',
            'first_name': 'Invalid',
            'surname': 'User',
            'role': 'Buddy',
            'preferred_language': 'German',
            'degree_level': 'Bachelors', 
            'app_matr_number': '12345', 
            'department': 'FB 1', 
            'country': 'randomCountry', 
            'preferred_number_of_partners': '2', 
            'is_permitted': 'true'
        }
        form = BuddyMatchingUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_form_valid(self):
        form_data = {
            'email': 'login.user@example.com',
            'password': 'password123!',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = BuddyMatchingUser.objects.create_user(
            email='test.user@example.com',
            password='password123!'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation_view_get(self):
        response = self.client.get(reverse('create_account_view'))
        self.assertEqual(response.status_code, 200)

    def test_account_creation_view_post_valid(self):
        form_data = {
            'email': 'new.user@example.com',
            'password1': 'password123!',
            'password2': 'password123!',
            'first_name': 'New',
            'surname': 'User',
            'role': 'Buddy',
            'preferred_language': 'German',
            'degree_level': 'Bachelors', 
            'app_matr_number': '12345', 
            'department': 'FB 1', 
            'country': 'randomCountry', 
            'preferred_number_of_partners': '2', 
            'is_permitted': 'true'
            
        }
        response = self.client.post(reverse('create_account_view'), data=form_data)
        self.assertEqual(response.status_code, 201)

    def test_account_creation_view_post_invalid(self):
        form_data = {
            'email': 'new.user@example.com',
            'password1': 'password123!',
            'password2': 'password456!',
        }
        response = self.client.post(reverse('create_account_view'), data=form_data)
        self.assertEqual(response.status_code, 400)

    def test_login_view_valid(self):
        response = self.client.post(reverse('login'), data={
            'email': 'test.user@example.com',
            'password': 'password123!'
        })
       
        self.assertEqual(response.status_code, 302) # Redirect to homepage
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_view_invalid(self):
        response = self.client.post(reverse('login'), data={
            'email': 'test.user@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check for proper error handling
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(email='test.user@example.com', password='password123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to homepage
