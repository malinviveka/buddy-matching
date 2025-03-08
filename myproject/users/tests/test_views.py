from django.test import TestCase, Client
from django.urls import reverse
from users.models import BuddyMatchingUser
from users.forms import BuddyMatchingUserCreationForm
import json


class AccountCreationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("create_account_view")

    def test_account_creation_page_loads(self):
        """Test if the account creation page loads correctly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/account_creation.html")

    def test_account_creation_valid_data(self):
        """Test form submission with valid data"""
        form_data = {
            "email": "valid@example.com",
            "password1": "password123!",
            "password2": "password123!",
            "first_name": "Valid",
            "surname": "User",
            "role": "Buddy",
            "preferred_language": "German",
            "degree_level": "Bachelors",
            "app_matr_number": "123456",
            "department": "FB 1",
            "country": "DE",
            "preferred_number_of_partners": 2,
            "is_permitted": "true",
            "interests": [],
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Account created successfully!", response.json()["message"])
        self.assertTrue(
            BuddyMatchingUser.objects.filter(email=form_data["email"]).exists()
        )

    def test_account_creation_invalid_data(self):
        """Test form submission with invalid data (password mismatch)"""
        form_data = {
            "role": "Student",
            "surname": "Doe",
            "first_name": "John",
            "email": "john.doe@example.com",
            "password1": "SecurePass123",
            "password2": "WrongPassword",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())
