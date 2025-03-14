from django.test import TestCase, Client
from django.urls import reverse
from users.models import BuddyMatchingUser

class AccountCreationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_account_view')

    def test_account_creation_page_loads(self):
        """Test if the account creation page loads correctly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/account_creation.html')

    def test_account_creation_valid_data(self):
        """Test form submission with valid data"""
        form_data = {
            'email': 'valid@example.com',
            'password1': 'password123!',
            'password2': 'password123!',
            'first_name': 'Valid',
            'surname': 'User',
            'role': 'Buddy',
            'preferred_language': 'German',
            'degree_level': 'Bachelors', 
            'app_matr_number': '123456', 
            'department': 'FB 1', 
            'country': 'DE', 
            'preferred_number_of_partners': 2, 
            'is_permitted': 'true',
            "interests": [],
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Account created successfully!", response.json()["message"])
        self.assertTrue(BuddyMatchingUser.objects.filter(email=form_data["email"]).exists())

    def test_account_creation_invalid_data(self):
        """Test form submission with invalid data (password mismatch)"""
        form_data = {
            "role": "Student",
            "surname": "Doe",
            "first_name": "John",
            "email": "john.doe@example.com",
            "password1": "SecurePass123",
            "password2": "WrongPassword"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())

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
        self.assertEqual(response.status_code, 400)

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