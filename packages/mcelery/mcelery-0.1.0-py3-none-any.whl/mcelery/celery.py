import os
from datetime import timedelta

from celery import Celery

celery_broker = os.environ.get("CELERY_BROKER")
celery_backend = os.environ.get("CELERY_BACKEND")
celery_app = Celery("tasks", broker=celery_broker, backend=celery_backend)

celery_app.conf.enable_utc = False
celery_app.conf.result_backend_always_retry = True
celery_app.conf.result_extended = True
celery_app.conf.result_expires = timedelta(days=7)
celery_app.conf.redis_backend_health_check_interval = 60
celery_app.conf.worker_send_task_events = True