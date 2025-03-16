from django.test import TestCase
from feedback.models import BuddyMatchingUser
from matching.matching_utils import calculate_match_score
from matching.matching import run_matching
from matching.matching import gale_shapley
from matching.matching_utils import create_preference_lists


class MatchingTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.buddy = BuddyMatchingUser.objects.create(
            role="Buddy",
            email="buddy@test.com",
            app_matr_number="666666",
            preferred_language="English",
            department="FB 20",
            country="Spain",
            preferred_number_of_partners=1,
            interests=["Sports"],
            degree_level="Bachelors",
        )

        self.student1 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student1@test.com",
            app_matr_number="777777",
            preferred_language="English",
            department="FB 20",
            country="Spain",
            interests=["Sports"],
            degree_level="Bachelors",
        )

        self.student2 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student2@test.com",
            app_matr_number="888888",
            preferred_language="English",
            department="FB 20",
            country="Spain",
            interests=["Sports"],
            degree_level="Bachelors",
        )
        self.student3 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student3@test.com",
            app_matr_number="999999",
            preferred_language="English",
            department="FB 20",
            country="Spain",
            interests=["Sports"],
            degree_level="Bachelors",
        )

    def test_preferred_number_of_partners(self):
        """Test if the buddy gets only the preferred number of partners."""

        buddies = BuddyMatchingUser.objects.filter(role="Buddy")
        students = BuddyMatchingUser.objects.filter(role="International Student")

        student_preferences, buddy_preferences = create_preference_lists(
            students, buddies
        )
        matches = gale_shapley(
            students, buddies, student_preferences, buddy_preferences
        )

        self.assertEqual(len(matches[self.buddy]), 1)

    def test_more_students_than_buddies(self):
        """Tests if the case where more students exist than buddies is handled correctly."""

        buddies = BuddyMatchingUser.objects.filter(role="Buddy")
        students = BuddyMatchingUser.objects.filter(role="International Student")

        # Create preference lists for students and buddies
        student_preferences, buddy_preferences = create_preference_lists(
            students, buddies
        )

        # Run the Gale-Shapley algorithm to get the matches
        matches = gale_shapley(
            students, buddies, student_preferences, buddy_preferences
        )

        # Buddy should only have one match because they want only one partner
        self.assertEqual(len(matches[self.buddy]), 1)

        # Check that the buddy was matched with one of the students
        self.assertIn(
            self.student1, matches[self.buddy]
        )  # Example: Buddy should match with student1

        # Check if the students were matched correctly (there are more students than buddies)
        self.assertIn(self.student1, matches[self.buddy])

        # Since there are more students than buddies, some students should not be matched
        # Check that student2 and student3 do not have a match
        self.assertNotIn(
            self.student2, matches[self.buddy]
        )  # student2 should have no match
        self.assertNotIn(
            self.student3, matches[self.buddy]
        )  # student3 should have no matc


class MatchingTestCase2(TestCase):
    def setUp(self):
        # set up dummy buddies and students
        self.buddy1 = BuddyMatchingUser.objects.create(
            role="Buddy",
            email="buddy1@test.com",
            app_matr_number="111111",
            preferred_language="English",
            department="FB 20",
            country="Spain",
            preferred_number_of_partners=2,
            interests=["Sports", "Culture"],
            degree_level="Bachelors",
        )
        self.buddy2 = BuddyMatchingUser.objects.create(
            role="Buddy",
            email="buddy2@test.com",
            app_matr_number="222222",
            preferred_language="Both",
            department="FB 20",
            country="Italy",
            preferred_number_of_partners=1,
            interests=["Nature"],
            degree_level="Masters",
        )

        # set up dummy international students 
        self.student1 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student1@test.com",
            app_matr_number="333333",
            preferred_language="English",
            country="Spain",
            department="FB 20",
            interests=["Sports", "Nature"],
            degree_level="Masters",
        )
        self.student2 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student2@test.com",
            app_matr_number="444444",
            preferred_language="English",
            department="FB 20",
            country="Italy",
            interests=["Culture", "Nature"],
            degree_level="Bachelors",
        )
        self.student3 = BuddyMatchingUser.objects.create(
            role="International Student",
            email="student3@test.com",
            app_matr_number="555555",
            preferred_language="German",
            department="FB 16",
            country="Norway",
            interests=["Technology"],
            degree_level="Masters",
        )

    # test the calculation of the match score
    def test_calculate_match_score(self):
        score1 = calculate_match_score(self.buddy1, self.student1)
        self.assertEqual(score1, 10**4 + 10**3 + 10**2 + 10**1)  # 11110
        score2 = calculate_match_score(self.buddy1, self.student2)
        self.assertEqual(score2, 10**4 + 10**2 + 10**1 + 10**0)  # 10111
        score3 = calculate_match_score(self.buddy1, self.student3)
        self.assertEqual(score3, 0)

        score4 = calculate_match_score(self.buddy2, self.student1)
        self.assertEqual(score4, 10**4 + 10**2 + 10**1 + 10**0)  # 10111
        score5 = calculate_match_score(self.buddy2, self.student2)
        self.assertEqual(score5, 10**4 + 10**3 + 10**2 + 10**1)  # 11110
        score6 = calculate_match_score(self.buddy2, self.student3)
        self.assertEqual(score6, 10**4 + 10**0)  # 10001

    # test the creation of the preference lists
    def test_create_preference_lists(self):
        buddies = BuddyMatchingUser.objects.filter(role="Buddy")
        students = BuddyMatchingUser.objects.filter(role="International Student")

        # Call the method to create preference lists
        student_preferences, buddy_preferences = create_preference_lists(
            students, buddies
        )

        # Check student preferences
        self.assertEqual(
            student_preferences[self.student1],
            [(self.buddy1, 11110), (self.buddy2, 10111)],
        )
        self.assertEqual(
            student_preferences[self.student2],
            [(self.buddy2, 11110), (self.buddy1, 10111)],
        )
        self.assertEqual(
            student_preferences[self.student3], [(self.buddy2, 10001), (self.buddy1, 0)]
        )

        # Check buddy preferences
        self.assertEqual(
            buddy_preferences[self.buddy1],
            [(self.student1, 11110), (self.student2, 10111), (self.student3, 0)],
        )
        self.assertEqual(
            buddy_preferences[self.buddy2],
            [(self.student2, 11110), (self.student1, 10111), (self.student3, 10001)],
        )

    # test the Gale-Shapley algorithm
    def test_gale_shapley(self):
        buddies = BuddyMatchingUser.objects.filter(role="Buddy")
        students = BuddyMatchingUser.objects.filter(role="International Student")

        student_preferences, buddy_preferences = create_preference_lists(
            students, buddies
        )

        matches = gale_shapley(
            students, buddies, student_preferences, buddy_preferences
        )

        # check if matches are correct
        self.assertIn(self.student1, matches[self.buddy1])
        self.assertIn(self.student2, matches[self.buddy2])
        self.assertIn(self.student3, matches[self.buddy1])

        # buddy2 should only have one match
        self.assertEqual(len(matches[self.buddy2]), 1)

    # test the whole matching process
    def test_run_matching(self):
        run_matching()

        # Note: Django saves Many-to-Many-relations as QuerySets, remember to use the `.all()` method to retrieve the related objects

        # check if the matches are stored in the database
        self.assertIn(self.student2, self.buddy2.partners.all())
        self.assertIn(self.student1, self.buddy1.partners.all())
        self.assertIn(self.student2, self.buddy2.partners.all())
        self.assertIn(self.student3, self.buddy1.partners.all())

        # Optional: test the reciprocity of the matches
        self.assertIn(self.buddy2, self.student2.partners.all())
        self.assertIn(self.buddy1, self.student1.partners.all())
        self.assertIn(self.buddy1, self.student3.partners.all())
