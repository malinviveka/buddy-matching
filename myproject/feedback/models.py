from django.db import models
from django.utils.timezone import now
from datetime import timedelta

FeedbackLifetime = 183 # Sets default date until account deletion in days. Default is 183 (half a year).
def default_deletion_date():
    return now().date() + timedelta(days=FeedbackLifetime)

class Feedback(models.Model):
    '''
    Model to store feedback from students.
    '''
    RATING_CHOICES = [
        ('EX', 'Excellent'),
        ('VG', 'Very Good'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
        ('NA', 'N/A'),
    ]

    #student = models.ForeignKey(BuddyMatchingUser, on_delete=models.CASCADE)  # Link to BuddyMatchingUser
    student_email = models.EmailField(help_text="Email of the student who submitted the feedback.", default="Email Not Found")

    text_feedback = models.TextField(blank=True, help_text="Provide your detailed feedback.")
    rating_1 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate your experience.")
    rating_2 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate the matching process.")
    # Add more rating fields

    # Automatically set the date and time when the feedback is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["submitted_at"]),
        ]
    
    def __str__(self):
        return f"Feedback from {self.student_email} on {self.submitted_at}"