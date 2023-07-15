import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "parser:lalafo": {
        "task": "hsearch.parser.tasks.parse_lalafo",
        "schedule": crontab(),
    },
}
