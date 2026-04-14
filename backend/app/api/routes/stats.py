from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import ActionItem, Meeting

router = APIRouter(prefix="/stats")


@router.get("/home")
def home_stats(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=7)

    meetings_this_week = db.query(Meeting).filter(Meeting.created_at >= week_start).count()
    pending_tasks = db.query(ActionItem).filter(ActionItem.status != "done").count()

    return {
        "total_meetings_this_week": meetings_this_week,
        "pending_tasks": pending_tasks,
    }
