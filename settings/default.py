import os
import sys
from os.path import abspath, join, curdir
from boto.s3.connection import S3Connection, SubdomainCallingFormat
from boto.s3.key import Key


DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Levi Thomason', 'me@levithomason.com'),
)

MANAGERS = ADMINS + (
    ('Jerica Thomason', 'jerica@sparrowbleuphotography.com'),
)

SUPERUSER_NAME = os.environ.get('SUPERUSER_NAME', 'admin')
SUPERUSER_EMAIL = os.environ.get('SUPERUSER_EMAIL', 'admin@sparrowbleu.com')
SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'admin')

POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY', None)
POSTMARK_SENDER = os.environ.get('POSTMARK_SENDER', None)
POSTMARK_TEST_MODE = DEBUG

SERVER_EMAIL = POSTMARK_SENDER
EMAIL_SUBJECT_PREFIX = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Static asset configuration
PROJECT_PATH = abspath(curdir)

# Append '/apps/' dir to PYTHON_PATH so we don't have to do 'apps.sparrow_bleu'
sys.path.append(join(PROJECT_PATH, 'apps'))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'mediafiles')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*blhedyelf3m-y90by&0@4ta0&6$k#@70qy93dn#-2&or5d(l1'

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)


# boto
boto_conn = S3Connection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
boto_bucket = boto_conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
boto_key = Key(boto_bucket)

# Storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_CALLING_FORMAT = SubdomainCallingFormat

# sorl thumbnail
THUMBNAIL_PREFIX = 'thumbs/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH,
    join(PROJECT_PATH, 'apps/sparrow_bleu/templates/'),
    join(PROJECT_PATH, 'apps/galleries/templates/'),
    join(PROJECT_PATH, 'apps/user/templates/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'apps.sparrow_bleu.urls'


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

INTERNAL_IPS = ('',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',

    'user',
    'sparrow_bleu',
    'galleries',

    'south',
    'sorl.thumbnail',
    'gunicorn',
    'storages',
    'endless_pagination',
    'django_extensions',
    'django_nose',
)

ENDLESS_PAGINATION_PREVIOUS_LABEL = '<i class="fa fa-chevron-left"></i>'
ENDLESS_PAGINATION_NEXT_LABEL = '<i class="fa fa-chevron-right"></i>'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
