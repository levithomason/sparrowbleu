from __future__ import absolute_import
import os
from celery import Celery, task
from django.conf import settings

app = Celery()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

# scan installed apps for tasks.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
