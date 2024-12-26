from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorconnect.settings")

app = Celery("tutorconnect")

app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

logger = logging.getLogger(__name__)


@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {self.request!r}")
