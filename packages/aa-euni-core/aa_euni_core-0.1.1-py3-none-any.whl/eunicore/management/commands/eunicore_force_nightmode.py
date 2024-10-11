# Django
from django.core.management.base import BaseCommand

# Alliance Auth
from allianceauth.authentication.models import UserProfile


class Command(BaseCommand):
    help = "Sets all users profiles to be night_mode = True"

    def handle(self, *args, **options):
        UserProfile.objects.update(night_mode=True)
