from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from .celery_schedule_conf import CELERYBEAT_SCHEDULE

from django.conf import settings
if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idcp_project.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idcp_project.settings.production")

app = Celery("idcp_project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = CELERYBEAT_SCHEDULE
