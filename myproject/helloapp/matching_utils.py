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
    # Dictionary to store the score for each (buddy, student) pair
    scores = {}

    # Calculate scores for all pairs and store them
    for buddy in buddies:
        for student in students:
            score = calculate_match_score(buddy, student)
            scores[(buddy, student)] = score

    # Create preference lists for students
    student_preferences = defaultdict(list)
    for student in students:
        student_preferences[student] = sorted(
            [(buddy, scores[(buddy, student)]) for buddy in buddies],
            key=lambda x: x[1],  # Sort by score
            reverse=True  # Descending order
        )

    # Create preference lists for buddies
    buddy_preferences = defaultdict(list)
    for buddy in buddies:
        buddy_preferences[buddy] = sorted(
            [(student, scores[(buddy, student)]) for student in students],
            key=lambda x: x[1],  # Sort by score
            reverse=True  # Descending order
        )

    return student_preferences, buddy_preferences