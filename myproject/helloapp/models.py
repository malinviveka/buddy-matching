from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta


class HomepageText(models.Model):
    content_de = models.TextField(_("Content in German"), default="Willkommen auf der Seite!")
    content_en = models.TextField(_("Content in English"), default="Welcome to the page!")
    last_updated = models.DateTimeField(auto_now=True)  # Wird bei jeder Änderung automatisch aktualisiert

    def __str__(self):
        return f"Homepage Text (aktualisiert am {self.last_updated})"
    


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

    student = models.ForeignKey(BuddyMatchingUser, on_delete=models.CASCADE)  # Link to BuddyMatchingUser
    text_feedback = models.TextField(blank=True, help_text="Provide your detailed feedback.")
    rating_1 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate your experience.")
    rating_2 = models.CharField(max_length=2, choices=RATING_CHOICES, help_text="Rate the matching process.")
    # Add more rating fields

    # Automatically set the date and time when the feedback is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Feedback from {self.student.email} on {self.submitted_at}"