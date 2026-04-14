from fastapi import APIRouter

from app.api.routes import action_items, events, meetings, stats, telegram

api_router = APIRouter()
api_router.include_router(telegram.router, tags=["telegram"])
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])
api_router.include_router(action_items.router, prefix="/action-items", tags=["action-items"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(stats.router, tags=["stats"])
