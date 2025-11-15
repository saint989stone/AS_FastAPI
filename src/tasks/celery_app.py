from celery import Celery

from src.config import settings
#celery --app=src.tasks.celery_app:celery_instance worker -l INFO --pool=solo


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"],
)

celery_instance.conf.beat_schedule = {
    "name_beatup": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}