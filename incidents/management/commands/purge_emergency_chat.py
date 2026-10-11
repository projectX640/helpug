from django.core.management.base import BaseCommand
from django.utils import timezone

from incidents.models import EmergencyChatRoom


class Command(BaseCommand):
    help = "Delete emergency chat rooms and their messages after the 48-hour retention window."

    def handle(self, *args, **options):
        deleted, _ = EmergencyChatRoom.objects.filter(expires_at__lte=timezone.now()).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} expired emergency chat records."))
