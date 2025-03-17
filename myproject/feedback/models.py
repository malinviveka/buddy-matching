from django.db import models
from django.utils.timezone import now
from users.models import BuddyMatchingUser # noqa: F401
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

FeedbackLifetime = 183  # Sets default date until account deletion in days. Default is 183 (half a year).


def default_deletion_date():
    return now().date() + timedelta(days=FeedbackLifetime)


class Feedback(models.Model):
    """
    Model to store feedback from students.
    """

    ROLE_CHOICES = [
        ("Student", _("Student")),
        ("Buddy", _("Buddy")),
    ]

    DISCOVERY_CHOICES = [
        ("Admission letter", _("Admission letter")),
        (
            "International Relations Unit website",
            _("International Relations Unit website")
        ),
        (
            "International Student Services website",
            _("International Student Services website")
        ),
        ("Orientation Programmes", _("Orientation Programmes")),
        ("Social-media channels", _("Social-media channels")),
        ("Friends and fellow students", _("Friends and fellow students")),
    ]

    SUPPORT_CHOICES = [
        ("Yes", _("Yes")),
        ("No", _("No")),
        ("I did not need any support", _("I did not need any support")),
    ]

    FIRST_CONTACT_CHOICES = [
        ("Late", _("Late")),
        ("Easy", _("Easy")),
        ("Difficult", _("Difficult")),
        ("I was never contacted", _("I was never contacted")),
    ]

    CONTACT_CHOICES = [
        ("Regular", _("Regular")),
        ("Low", _("Low")),
        ("Inexistent", _("Inexistent")),
    ]

    PROBLEMS_CHOICES = [
        ("Yes/Sometimes", _("Yes/Sometimes")),
        ("No", _("No")),
    ]

    RECOMMENDATION_CHOICES = [
        ("Yes", _("Yes")),
        ("No/Maybe", _("No/Maybe")),
    ]

    student_email = models.EmailField(
        help_text="Email of the student who submitted the feedback.",
        default="Email Not Found",
    )

    # See questions in html file
    q1 = models.CharField(max_length=7, choices=ROLE_CHOICES, null=True)
    q2 = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], null=True
    )  # On a scale of 1 to 5
    q3 = models.PositiveBigIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], null=True
    )
    q4 = models.CharField(max_length=100, choices=DISCOVERY_CHOICES, null=True)
    q5 = models.CharField(max_length=100, choices=SUPPORT_CHOICES, null=True)
    q5_details = models.TextField(blank=True)  # If support is needed, provide details
    q6 = models.CharField(max_length=100, choices=FIRST_CONTACT_CHOICES, null=True)
    q7 = models.CharField(max_length=100, choices=CONTACT_CHOICES, null=True)
    q8 = models.CharField(max_length=100, choices=PROBLEMS_CHOICES, null=True)
    q8_details = models.TextField(blank=True)  # If problems are faced, provide details
    q9 = models.CharField(max_length=100, choices=RECOMMENDATION_CHOICES, null=True)
    q9_details = models.TextField(blank=True)  # If would not recommend, provide details
    q10 = models.TextField(blank=True)

    # Automatically set the date and time when the feedback is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["submitted_at"]),
        ]

    def __str__(self):
        return f"Feedback from {self.student_email} on {self.submitted_at}"
