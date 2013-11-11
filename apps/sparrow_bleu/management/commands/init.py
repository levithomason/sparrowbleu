import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    args = ''
    help = 'Creates admin account and user profile to go with it'

    def handle(self, *args, **options):
        # Setup admin
        u = User.objects.get_or_create(username='admin')[0]
        u.set_password('admin')
        u.email = "admin@sbp.com"
        u.is_superuser = True
        u.is_staff = True
        u.save()

        try:
            u.get_profile()
        except ObjectDoesNotExist:
            #user_profile = UserProfile.objects.create(user=u)
            pass

        print "Created admin//admin"

        # Setup Facebook
        facebook, created = SocialApp.objects.get_or_create(
            provider="facebook",
            name="facebook",
            client_id=settings.FACEBOOK_API_CLIENT_ID,
            secret=settings.FACEBOOK_API_SECRET,
        )
        facebook.sites.add(Site.objects.get_current())

        print "Created SocialApp for Facebook"
