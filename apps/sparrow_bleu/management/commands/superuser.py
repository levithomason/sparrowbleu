from django.core.management.base import NoArgsCommand
from django.db import DEFAULT_DB_ALIAS as database
from django.contrib.auth.models import User
from django.conf import settings


class Command(NoArgsCommand):
    help = 'Create superuser from env variables'

    def handle_noargs(self, **options):
        User.objects.db_manager(database).create_superuser(settings.SUPERUSER_NAME, settings.SUPERUSER_EMAIL,
                                                           settings.SUPERUSER_PASSWORD)
