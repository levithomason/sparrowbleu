from django.core.management.base import NoArgsCommand
from django.db import DEFAULT_DB_ALIAS as database
from django.contrib.auth.models import User
from settings import SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD


class Command(NoArgsCommand):
    help = 'Create superuser from env variables'

    def handle_noargs(self, **options):
        User.objects.db_manager(database).create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)
