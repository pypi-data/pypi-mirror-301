import os

from celery import Celery

celery_broker = os.environ.get("CELERY_BROKER")
celery_backend = os.environ.get("CELERY_BACKEND")
celery_app = Celery("tasks", broker=celery_broker, backend=celery_backend)
