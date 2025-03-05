from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Feedback, BuddyMatchingUser
User = get_user_model()
class FeedbackTestCase(TestCase):
    def setUp(self):
        self.buddy = BuddyMatchingUser.objects.create_user(
            email='buddy@test.com', password='test123', role='Buddy',
            app_matr_number=2356
        )
        self.student = BuddyMatchingUser.objects.create_user(
            email='student@test.com', password='test123', role='International Student',
            app_matr_number=1234
        )
        self.buddy.partners.add(self.student)
        self.student.partners.add(self.buddy)

        # Create an admin user
        self.admin_user = BuddyMatchingUser.objects.create_user(
            email='admin@test.com', password='test123', role='Admin',
            app_matr_number=9999
        )
        self.admin_user.is_staff = True  # Make this user a staff member (admin)
        self.admin_user.save()

    def test_feedback_valid_submission(self):
        """test whether valid feedback is submitted"""
        # login as buddy
        self.client.login(email='buddy@test.com', password='test123')

        # POST call with valid feedback data
        response = self.client.post(reverse('submit_feedback'), {
            'student': self.student.id,  
            'rating_1': 'EX',  # valid feedback
            'rating_2': 'G',  # valid feedback
            'text_feedback': 'Sehr nette Person!',  
        })

        
        self.assertEqual(response.status_code, 201)

        
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.rating_1, 'EX')  
        self.assertEqual(feedback.rating_2, 'G') 
        self.assertEqual(feedback.text_feedback, 'Sehr nette Person!')  

    def test_feedback_invalid_submission(self):
        """test whether invalid values are rejected"""
        
        self.client.login(email='buddy@test.com', password='test123')

       
        self.client.post(reverse('submit_feedback'), { #removed response = as it is never used
            'student': self.student.id,
            'rating_1': 'Awesome',  # invalid rating
            'rating_2': 'G',  # valid rating
            'text_feedback': 'Nicht gültige Antwort!', 
        })

        

    def test_feedback_na_submission(self):
        """Tests if 'N/A' is accepted as a valid rating."""
        self.client.login(email='buddy@test.com', password='test123')
        response = self.client.post(reverse('submit_feedback'), {
            'student': self.student.id,
            'rating_1': 'NA',  # 'N/A' as a rating
            'rating_2': 'NA',
            'text_feedback': 'No comment.',
        })
        self.assertEqual(response.status_code, 201)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.rating_1, 'NA')  # Check if 'N/A' is saved correctly

    def test_multiple_feedback_submission(self):
        """Tests if the same user can submit feedback multiple times."""
        self.client.login(email='buddy@test.com', password='test123')
        
        # First feedback submission
        response1 = self.client.post(reverse('submit_feedback'), {
            'student': self.student.id,
            'rating_1': 'EX',
            'rating_2': 'VG',
            'text_feedback': 'Very good feedback!',
        })
        self.assertEqual(response1.status_code, 201)
        
        # Second feedback submission
        response2 = self.client.post(reverse('submit_feedback'), {
            'student': self.student.id,
            'rating_1': 'G',
            'rating_2': 'F',
            'text_feedback': 'Improvement potential!',
        })
        self.assertEqual(response2.status_code, 201)
        
        feedback_count = Feedback.objects.count()
        self.assertEqual(feedback_count, 2)  # Both feedbacks should be saved





   
