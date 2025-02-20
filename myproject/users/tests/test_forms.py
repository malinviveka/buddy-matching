from django.test import TestCase
from users.forms import BuddyMatchingUserCreationForm

class AccountCreationFormTests(TestCase):
    def test_valid_form(self):
        """Test if the form is valid with correct data"""
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
        form = BuddyMatchingUserCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Test form validation with an invalid email"""
        form_data = {
            "email": "not-an-email",
            "password1": "SecurePass123",
            "password2": "SecurePass123"
        }
        form = BuddyMatchingUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
