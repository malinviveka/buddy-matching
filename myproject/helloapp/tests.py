from django.test import TestCase
from django.urls import reverse
from .models import BuddyMatchingUser
from .forms import BuddyMatchingUserCreationForm, LoginForm
from .matching import run_matching, gale_shapley
from .matching_utils import create_preference_lists, calculate_match_score
from collections import defaultdict

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


# tests for matching algorithm
class MatchingTestCase(TestCase):
    def setUp(self):
        # set up dummy buddies and students
        self.buddy1 = BuddyMatchingUser.objects.create(
            role='Buddy',
            email='buddy1@test.com',
            app_matr_number='111111',
            preferred_language='English',
            department='FB 20',
            country='Spain',
            preferred_number_of_partners=2,
            interests=['Sports', 'Culture'],
            degree_level='Bachelors'
        )
        self.buddy2 = BuddyMatchingUser.objects.create(
            role='Buddy',
            email='buddy2@test.com',
            app_matr_number='222222',
            preferred_language='Both',
            department='FB 20',
            country='Italy',
            preferred_number_of_partners=1,
            interests=['Nature'],
            degree_level='Masters'
        )

        # Dummy Internationale Studierende erstellen
        self.student1 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student1@test.com',
            app_matr_number='333333',
            preferred_language='English',
            country='Spain',
            department='FB 20',
            interests=['Sports', 'Nature'],
            degree_level='Masters'
        )
        self.student2 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student2@test.com',
            app_matr_number='444444',
            preferred_language='English',
            department='FB 20',
            country='Italy',
            interests=['Culture', 'Nature'],
            degree_level='Bachelors'
        )
        self.student3 = BuddyMatchingUser.objects.create(
            role='International Student',
            email='student3@test.com',
            app_matr_number='555555',
            preferred_language='German',
            department='FB 16',
            country='Norway',
            interests=['Technology'],
            degree_level='Masters'
        )

    # test the calculation of the match score
    def test_calculate_match_score(self):
        score1 = calculate_match_score(self.buddy1, self.student1)
        self.assertEqual(score1, 7) 
        score2 = calculate_match_score(self.buddy1, self.student2)
        self.assertEqual(score2, 5.5)  
        score3 = calculate_match_score(self.buddy1, self.student3)
        self.assertEqual(score3, 0) 

        score4 = calculate_match_score(self.buddy2, self.student1)
        self.assertEqual(score4, 5.5)
        score5 = calculate_match_score(self.buddy2, self.student2)
        self.assertEqual(score5, 7)
        score6 = calculate_match_score(self.buddy2, self.student3)
        self.assertEqual(score6, 3.5)


    # test the creation of the preference lists
    def test_create_preference_lists(self):
        buddies = BuddyMatchingUser.objects.filter(role='Buddy')
        students = BuddyMatchingUser.objects.filter(role='International Student')

        print("BUDDIES: ", buddies)   # debug
        print("STUDENTS: ", students)   # debug
        
        # Call the method to create preference lists
        student_preferences, buddy_preferences = create_preference_lists(buddies, students)

        print("STUDENT PREFERENCES: ", student_preferences)   # debug
        print("BUDDY PREFERENCES: ", buddy_preferences)   # debug

        # Check student preferences
        self.assertEqual(student_preferences[self.student1], [
            (self.buddy1, 7),
            (self.buddy2, 5.5)
        ])
        self.assertEqual(student_preferences[self.student2], [
            (self.buddy2, 7),
            (self.buddy1, 5.5)
        ])
        self.assertEqual(student_preferences[self.student3], [
            (self.buddy2, 3.5),
            (self.buddy1, 0)
        ])

        # Check buddy preferences
        self.assertEqual(buddy_preferences[self.buddy1], [
            (self.student1, 7),
            (self.student2, 5.5),
            (self.student3, 0)
        ])
        self.assertEqual(buddy_preferences[self.buddy2], [
            (self.student2, 7),
            (self.student1, 5.5),
            (self.student3, 3.5)
        ])



    # test the Gale-Shapley algorithm
    def test_gale_shapley(self):
        buddies = BuddyMatchingUser.objects.filter(role='Buddy')
        students = BuddyMatchingUser.objects.filter(role='International Student')


        student_preferences, buddy_preferences = create_preference_lists(buddies, students)
        
        matches = gale_shapley(students, buddies, student_preferences, buddy_preferences)

    
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

        # Optional: Test die Gegenseitigkeit der Verknüpfungen
        self.assertIn(self.buddy2, self.student2.partners.all())
        self.assertIn(self.buddy1, self.student1.partners.all())
        self.assertIn(self.buddy1, self.student3.partners.all())
        

