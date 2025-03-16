# feedback/management/commands/delete_old_feedback.py

from django.core.management.base import BaseCommand
from feedback.models import Feedback
from django.utils.timezone import now
from datetime import timedelta


class Command(BaseCommand):
    help = "Deletes all feedback entries older than 6 months."

    def handle(self, *args, **kwargs):
        """
        Deletes feedback that is older than 183 days (6 months).

        Steps:
        1. Calculate the date threshold.
        2. Query and count feedback older than this date.
        3. Delete the feedback and print a success message.
        4. If no feedback is found, print a warning message.
        """
        expiration_date = now() - timedelta(days=183)  # Calculate expiration date 
        old_feedback = Feedback.objects.filter(submitted_at__lt=expiration_date)

        count = old_feedback.count()

        if count > 0:
            old_feedback.delete()
            self.stdout.write(
                self.style.SUCCESS(f"{count} old feedback entries deleted.")
            )
        else:
            self.stdout.write(self.style.WARNING("No old feedback entries found."))
