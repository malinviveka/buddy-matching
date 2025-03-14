from django.test import TestCase
from users.models import BuddyMatchingUser


class ModelsTestCase(TestCase):
    def test_buddy_matching_user_creation(self):
        user = BuddyMatchingUser.objects.create_user(
            email="john.doe@example.com",
            password="password123!",
            role="Buddy",
            first_name="John",
            surname="Doe",
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertTrue(user.check_password("password123!"))
