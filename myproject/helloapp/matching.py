from helloapp.models import BuddyMatchingUser
from .matching_utils import create_preference_lists
from collections import defaultdict, deque
from django.db import transaction
from django.db.models import Count, F

# student = international student

def gale_shapley(students, buddies, student_preferences, buddy_preferences):
    '''
    Run the Gale-Shapley algorithm to find stable matches between students and buddies.
    :param students: List of students
    :param buddies: List of buddies
    :param student_preferences: Dictionary of student preference lists
    :param buddy_preferences: Dictionary of buddy preference lists
    '''

    # Initialize variables
    unmatched_students = deque(students)  # Deque of students who have not yet been matched

    matches = defaultdict(list) # Buddy -> [Students]

    while unmatched_students:
        student = unmatched_students.popleft()  # get the first unmatched student
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
    buddies = BuddyMatchingUser.objects.filter(role='Buddy', is_permitted=True, is_staff=False).annotate(partner_count=Count('partners')).filter(preferred_number_of_partners__gte=F('partner_count'))
    students = BuddyMatchingUser.objects.filter(role='International Student', is_permitted=True, is_staff=False).annotate(partner_count=Count('partners')).filter(partner_count=0)
  
    # create preference lists
    student_preferences, buddy_preferences = create_preference_lists(students, buddies)
    
    # run Gale-Shapley 
    matches = gale_shapley(students, buddies, student_preferences, buddy_preferences)


    # safe matches in database
    with transaction.atomic():
        for buddy, students in matches.items():
            # add students to buddy
            buddy.partners.add(*students)
            # for each student add buddy
            for student in students:
                student.partners.add(buddy)

            # save buddy (update the partner count)
            buddy.save()

            # save students (update the partner count)
            for student in students:
                student.save()
    print(f"Successfully completed matching with {len(matches)} matches.")            