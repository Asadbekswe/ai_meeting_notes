from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "meeting_notes",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)
celery_app.conf.task_routes = {
    "app.workers.tasks.process_meeting": {"queue": "meetings"},
    "app.workers.tasks.send_reminders": {"queue": "reminders"},
}

# Ensure task decorators execute during worker startup.
import app.workers.tasks  # noqa: E402,F401
