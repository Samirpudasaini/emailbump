from celery import Celery
from app.core.config import settings

celery = Celery(
    "email_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_acks_late=True,           # only ack after success
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,  # fair dispatch
    task_routes={
        "app.tasks.email_tasks.send_email_task": {"queue": "email"},
    },
)