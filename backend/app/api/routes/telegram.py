from fastapi import APIRouter, Header, HTTPException

from app.core.config import settings
from app.workers.tasks import process_meeting

router = APIRouter(prefix="/telegram")


@router.post("/webhook")
def telegram_webhook(update: dict, x_telegram_bot_api_secret_token: str | None = Header(default=None)):
    if settings.telegram_webhook_secret and x_telegram_bot_api_secret_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    process_meeting.delay(update)
    return {"ok": True}
