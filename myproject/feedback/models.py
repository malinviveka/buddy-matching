from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import BuddyMatchingUser


class Feedback(models.Model):
    '''
    Model to store feedback from students.
    '''
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Buddy', 'Buddy'),
    ]

    DISCOVERY_CHOICES = [
        ('Admission letter', 'Admission letter'),
        ('International Relations Unit website', 'International Relations Unit website'),
        ('International Student Services website', 'International Student Services website'),
        ('Orientation Programmes', 'Orientation Programmes'),
        ('Social-media channels', 'Social-media channels'),
        ('Friends and fellow students', 'Friends and fellow students'),
    ]

    SUPPORT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('I did not need any support', 'I did not need any support'),
    ]

    FIRST_CONTACT_CHOICES = [
        ('Late', 'Late'),
        ('Easy', 'Easy'),
        ('Difficult', 'Difficult'),
        ('I was never contacted', 'I was never contacted'),
    ]

    CONTACT_CHOICES = [
        ('Regular', 'Regular'),
        ('Low', 'Low'),
        ('Inexistent', 'Inexistent'),
    ]

    PROBLEMS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Sometimes', 'Sometimes'),
    ]

    RECOMMENDATION_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Maybe', 'Maybe'),
    ]


    student = models.ForeignKey(BuddyMatchingUser, on_delete=models.CASCADE)  # Link to BuddyMatchingUser

    # See questions in html file
    q1 = models.CharField(max_length=7, choices=ROLE_CHOICES, null=True)
    q2 = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True) # On a scale of 1 to 5
    q3 = models.PositiveBigIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    q4 = models.CharField(max_length=100, choices=DISCOVERY_CHOICES, null=True)
    q5 = models.CharField(max_length=100, choices=SUPPORT_CHOICES, null=True)
    q5_details = models.TextField(blank=True) # If support is needed, provide details
    q6 = models.CharField(max_length=100, choices=FIRST_CONTACT_CHOICES, null=True)
    q7 = models.CharField(max_length=100, choices=CONTACT_CHOICES, null=True)
    q8 = models.CharField(max_length=100, choices=PROBLEMS_CHOICES, null=True)
    q8_details = models.TextField(blank=True) # If problems are faced, provide details
    q9 = models.CharField(max_length=100, choices=RECOMMENDATION_CHOICES, null=True)
    q9_details = models.TextField(blank=True) # If would not recommend, provide details
    q10 = models.TextField(blank=True)

    # Automatically set the date and time when the feedback is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Feedback from {self.student.email} on {self.submitted_at}"