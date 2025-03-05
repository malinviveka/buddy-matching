

from django.test import TestCase
from feedback.models import BuddyMatchingUser  
from matching.matching import gale_shapley
from matching.matching_utils import create_preference_lists

class MatchingTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.buddy = BuddyMatchingUser.objects.create(
            role='Buddy',
            email='buddy@test.com',
            app_matr_number='666666',
            preferred_language='English',
            department='FB 20',
            country='Spain',
            preferred_number_of_partners=1,  
            interests=['Sports'],
            degree_level='Bachelors'
        )
        
        self.student1 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student1@test.com',
            app_matr_number='777777',
            preferred_language='English',
            department='FB 20',
            country='Spain',
            interests=['Sports'],
            degree_level='Bachelors'
        )

        self.student2 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student2@test.com',
            app_matr_number='888888',
            preferred_language='English',
            department='FB 20',
            country='Spain',
            interests=['Sports'],
            degree_level='Bachelors'
        )
        self.student3 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student3@test.com',
            app_matr_number='999999',
            preferred_language='English',
            department='FB 20',
            country='Spain',
            interests=['Sports'],
            degree_level='Bachelors'
        )
        
    def test_preferred_number_of_partners(self):
        """Test if the buddy gets only the preferred number of partners."""
       
        buddies = BuddyMatchingUser.objects.filter(role='Buddy')
        students = BuddyMatchingUser.objects.filter(role='International Student')
        
        student_preferences, buddy_preferences = create_preference_lists(students, buddies)
        matches = gale_shapley(students, buddies, student_preferences, buddy_preferences)
        
       
        self.assertEqual(len(matches[self.buddy]), 1)  


    def test_more_students_than_buddies(self):
        """Tests if the case where more students exist than buddies is handled correctly."""

        buddies = BuddyMatchingUser.objects.filter(role='Buddy')
        students = BuddyMatchingUser.objects.filter(role='International Student')
        
        # Create preference lists for students and buddies
        student_preferences, buddy_preferences = create_preference_lists(students, buddies)
        
        # Run the Gale-Shapley algorithm to get the matches
        matches = gale_shapley(students, buddies, student_preferences, buddy_preferences)
        
        # Buddy should only have one match because they want only one partner
        self.assertEqual(len(matches[self.buddy]), 1)

        # Check that the buddy was matched with one of the students
        self.assertIn(self.student1, matches[self.buddy])  # Example: Buddy should match with student1

        # Check if the students were matched correctly (there are more students than buddies)
        self.assertIn(self.student1, matches[self.buddy])
        
        # Since there are more students than buddies, some students should not be matched
        # Check that student2 and student3 do not have a match
        self.assertNotIn(self.student2, matches[self.buddy])  # student2 should have no match
        self.assertNotIn(self.student3, matches[self.buddy])  # student3 should have no matc

