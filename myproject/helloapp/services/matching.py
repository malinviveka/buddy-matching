from helloapp.models import BuddyMatchingUser
from .matching_utils import create_preference_lists
from collections import defaultdict

def gale_shapley(buddies, students, preference_lists):
    matches = defaultdict(list)  # Buddy -> [Students]
    buddy_capacities = {buddy: buddy.preferred_number_of_partners for buddy in buddies}

    free_students = list(students)  # Liste der freien Studierenden

    # Matching-Schleife
    while free_students:
        student = free_students.pop(0)  # choose first student from list

        # get preference list of student
        for buddy, _ in preference_lists[student]:
            if len(matches[buddy]) < buddy_capacities[buddy]:
                # buddy has capacity left -> match student with buddy
                matches[buddy].append(student)
                break
            else:
                # check, if current Buddy would prefer different match
                current_students = matches[buddy]
                worst_student = min(
                    current_students,
                    key=lambda s: next(score for b, score in preference_lists[s] if b == buddy)
                )

                # if student is preferred over worst_student, match student with buddy
                new_score = next(score for b, score in preference_lists[student] if b == buddy)
                worst_score = next(score for b, score in preference_lists[worst_student] if b == buddy)

                if new_score > worst_score:
                    matches[buddy].remove(worst_student)
                    matches[buddy].append(student)
                    free_students.append(worst_student)
                    break
    return matches


def run_matching():
    # load data
    buddies = BuddyMatchingUser.objects.filter(role='Buddy', is_permitted=True)
    students = BuddyMatchingUser.objects.filter(role='International Student', is_permitted=True)
    
    # create preference lists
    preference_lists = create_preference_lists(buddies, students)
    
    # run Gale-Shapley 
    matches = gale_shapley(buddies, students, preference_lists)

    # safe matches in database
    for buddy, matched_students in matches.items():
        buddy.partners.set(matched_students)
        buddy.save()
