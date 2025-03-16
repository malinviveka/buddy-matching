from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Feedback, BuddyMatchingUser

User = get_user_model()


class FeedbackTestCase(TestCase):
    def setUp(self):
        self.buddy = BuddyMatchingUser.objects.create_user(
            email="buddy@test.com",
            password="test123",
            role="Buddy",
            app_matr_number=2356,
        )
        self.student = BuddyMatchingUser.objects.create_user(
            email="student@test.com",
            password="test123",
            role="International Student",
            app_matr_number=1234,
        )
        self.buddy.partners.add(self.student)
        self.student.partners.add(self.buddy)

        # Create an admin user
        self.admin_user = BuddyMatchingUser.objects.create_user(
            email="admin@test.com",
            password="test123",
            role="Admin",
            app_matr_number=9999,
        )
        self.admin_user.is_staff = True  # Make this user a staff member (admin)
        self.admin_user.save()

    def test_feedback_valid_submission(self):
        """test whether valid feedback is submitted"""
        # login as buddy
        self.client.login(email="buddy@test.com", password="test123")

        # POST call with valid feedback data
        response = self.client.post(
            reverse("submit_feedback"),
            {
                "student": self.student.id,
                "q1": "Student",
                "q2": "5",
                "q3": "5",
                "q4": "Admission letter",
                "q5": "I did not need any support",
                "q6": "Easy",
                "q7": "Regular",
                "q8": "No",
                "q9": "Yes",
                "q10": "No comment.",

            },
        )

        self.assertEqual(response.status_code, 201)

        feedback = Feedback.objects.first()
        self.assertEqual(feedback.q1, "Student")
        self.assertEqual(feedback.q2, 5)
        self.assertEqual(feedback.q3, 5)
        self.assertEqual(feedback.q4, "Admission letter")
        self.assertEqual(feedback.q5, "I did not need any support")
        self.assertEqual(feedback.q6, "Easy")
        self.assertEqual(feedback.q7, "Regular")
        self.assertEqual(feedback.q8, "No")
        self.assertEqual(feedback.q9, "Yes")
        self.assertEqual(feedback.q10, "No comment.")
        
    def test_feedback_invalid_submission(self):
        """Test whether invalid feedback is rejected"""
        response = self.client.post(
            reverse("submit_feedback"),
            {
                "student": self.student.id,
                "q1": "InvalidRole",  # Invalid choice
                "q2": "6",  # Out of range (valid range is 1-5)
                "q3": "-1",  # Negative number, invalid
                "q4": "Unknown Source",  # Not in DISCOVERY_CHOICES
                "q5": "Maybe",  # Not in SUPPORT_CHOICES
                "q6": "",  # Missing required field
                "q7": "Regular",
                "q8": "Sometimes",
                "q9": "Yes",
                "q10": "",
            },
        )

        self.assertNotEqual(response.status_code, 201)  # Expecting failure
        self.assertEqual(Feedback.objects.count(), 0)  # No feedback should be saved

    
    def test_multiple_feedback_submission(self):
        """Test whether the same user can submit feedback multiple times"""
        self.client.login(email="buddy@test.com", password="test123")
        feedback_data = {
            "student": self.student.id,
            "q1": "Student",
            "q2": "5",
            "q3": "5",
            "q4": "Admission letter",
            "q5": "I did not need any support",
            "q6": "Easy",
            "q7": "Regular",
            "q8": "No",
            "q9": "Yes",
            "q10": "No comment.",
        }

        response1 = self.client.post(reverse("submit_feedback"), feedback_data)
        response2 = self.client.post(reverse("submit_feedback"), feedback_data)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(Feedback.objects.count(), 2)  # Ensure two submissions exist
