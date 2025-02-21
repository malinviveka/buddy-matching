# myproject/management/commands/delete_expired_accounts.py

from django.core.management.base import BaseCommand
from users.models import BuddyMatchingUser
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Deletes all user accounts whose deletion date has passed, except staff members."

    def handle(self, *args, **kwargs):
        """
        Find and delete all user accounts where the deletion date is in the past,
        while ensuring that staff members (is_staff=True) are excluded from deletion.

        Steps:
        1. Query all users whose deletion date is earlier than today.
        2. Exclude staff members from the deletion process.
        3. Count the number of users that will be deleted.
        4. Delete the selected users and print a success message.
        5. If no users are found, print a warning message.
        """
        expired_users = BuddyMatchingUser.objects.filter(
            deletion_date__lt=now().date(),  # Users with a past deletion date
        ).exclude(is_staff=True)  # Exclude staff members

        count = expired_users.count()

        if count > 0:
            expired_users.delete()
            self.stdout.write(self.style.SUCCESS(f"{count} expired user accounts have been deleted."))
        else:
            self.stdout.write(self.style.WARNING("No expired user accounts found."))