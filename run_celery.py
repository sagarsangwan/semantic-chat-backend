# run_celery.py
from celery import Celery

app = Celery("semantic_chat_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

if __name__ == "__main__":
    app.worker_main(["worker", "--loglevel=info", "--pool=solo"])
