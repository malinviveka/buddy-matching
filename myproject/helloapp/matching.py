from helloapp.models import BuddyMatchingUser
from .matching_utils import create_preference_lists
from collections import defaultdict
from django.db import transaction

# student = international student

def gale_shapley(students, buddies, student_preferences, buddy_preferences):
    '''
    Run the Gale-Shapley algorithm to find stable matches between students and buddies.
    :param students: List of students
    :param buddies: List of buddies
    :param student_preferences: Dictionary of student preference lists
    :param buddy_preferences: Dictionary of buddy preference lists
    :param buddy_capacities: Dictionary of buddy capacities
    '''

    # Initialize variables
    unmatched_students = list(students)  # List of students who have not yet been matched
    matches = defaultdict(list) # Buddy -> [Students]

    while unmatched_students:
        student = unmatched_students.pop(0)  # get the first unmatched student
        student_pref_list = student_preferences[student] # get the preference list of the student

        # iterate over the preference list of the student
        for buddy, _ in student_pref_list:
            # check if buddy has capacity
            if len(matches[buddy]) < buddy.preferred_number_of_partners:
                matches[buddy].append(student)
                break

            # check if buddy prefers the student over the worst student in the current matches
            lowest_score_student = min(
                matches[buddy],
                key=lambda s: next(score for b, score in buddy_preferences[buddy] if b == s)
            )
            new_score = next(score for b, score in buddy_preferences[buddy] if b == student)
            current_lowest_score = next(score for b, score in buddy_preferences[buddy] if b == lowest_score_student)

            # if buddy prefers the student over the worst student in the current matches then swap the students
            if new_score > current_lowest_score:
                matches[buddy].remove(lowest_score_student)
                matches[buddy].append(student)
                unmatched_students.append(lowest_score_student)
                break
        else:
            continue
    return matches
    


def run_matching():
    # load data
    buddies = BuddyMatchingUser.objects.filter(role='Buddy', is_permitted=True)
    students = BuddyMatchingUser.objects.filter(role='International Student', is_permitted=True)
    
    # create preference lists
    student_preferences, buddy_preferences = create_preference_lists(buddies, students)
    
    # run Gale-Shapley 
    matches = gale_shapley(buddies, students, student_preferences, buddy_preferences)

    # safe matches in database
    for buddy, matched_students in matches.items():
        buddy.partners.set(matched_students)
        buddy.save()