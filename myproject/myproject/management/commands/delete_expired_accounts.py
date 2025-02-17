# helloapp/management/commands/delete_expired_accounts.py

from django.core.management.base import BaseCommand
from users.models import BuddyMatchingUser
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Löscht alle Benutzerkonten, deren Löschdatum überschritten wurde.'

    def handle(self, *args, **kwargs):
        # Alle Benutzer finden, deren Löschdatum vor HEUTE liegt
        expired_users = BuddyMatchingUser.objects.filter(deletion_date__lt=now().date())
        count = expired_users.count()

        if count > 0:
            expired_users.delete()
            self.stdout.write(self.style.SUCCESS(f'{count} abgelaufene Benutzerkonten wurden gelöscht.'))
        else:
            self.stdout.write(self.style.WARNING('Keine abgelaufenen Benutzerkonten gefunden.'))