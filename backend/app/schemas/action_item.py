from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ActionItemUpdate(BaseModel):
    task_text: str | None = None
    owner_name_raw: str | None = None
    status: str | None = None


class ActionItemOut(BaseModel):
    id: UUID
    meeting_id: UUID
    task_text: str
    owner_name_raw: str | None
    status: str
    updated_at: datetime

    class Config:
        from_attributes = True
