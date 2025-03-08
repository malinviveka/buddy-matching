# from django.test import TestCase, Client
# from django.urls import reverse

# class AccountCreationTemplateTests(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_template_contains_form_elements(self):
#         """Check if the account creation form contains required fields"""
#         response = self.client.get(reverse('create_account_view'))
#         self.assertContains(response, '<form', status_code=200)
#         self.assertContains(response, '<input', count=18)  # Checks if all input fields are there. contains csrfmiddlewaretoken)
#         self.assertContains(response, '<button type="submit"', status_code=200)
