from collections import defaultdict


def calculate_match_score(buddy, student):
    score = 0
    # priorities can be changed later

    # language
    if buddy.preferred_language in ('Both', student.preferred_language):
        score += 3

    # country of sending university or country of preference
    if buddy.country.lower() == student.country.lower():
        score += 2

    # interests
    common_interests = set(buddy.interests).intersection(set(student.interests))
    score += len(common_interests)

    # department (at TU Darmstadt)
    if buddy.department == student.department:
        score += 1

    # degree level
    if buddy.degree_level == student.degree_level:
        score += 0.5

    return score



def create_preference_lists(buddies, students):
    # create preference lists for international students
    preference_lists = defaultdict(list)

    for student in students:
        for buddy in buddies:
            score = calculate_match_score(buddy, student)
            print(f"Score for {student} and {buddy}: {score}")  # Debugging
            if score > 0:  # only consider buddies with a score > 0
                preference_lists[student].append((buddy, score))
        
        # sort the preference list in descending order
        preference_lists[student].sort(key=lambda x: x[1], reverse=True)
