# celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semantic_chat_backend.settings")

app = Celery(
    "semantic_chat_backend",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
