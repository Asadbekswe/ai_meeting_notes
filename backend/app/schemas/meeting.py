from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MeetingCreate(BaseModel):
    source_type: str = "audio_file"
    title: str | None = None


class MeetingUpdate(BaseModel):
    title: str | None = None
    summary_text: str | None = None


class MeetingOut(BaseModel):
    id: UUID
    source_type: str
    title: str | None
    status: str
    summary_text: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class DecisionOut(BaseModel):
    text: str


class TopicOut(BaseModel):
    name: str


class MeetingActionItemOut(BaseModel):
    task_text: str
    owner_name_raw: str | None
    status: str


class MeetingDetailOut(BaseModel):
    id: UUID
    title: str | None
    status: str
    summary_text: str | None
    transcript: str | None
    decisions: list[DecisionOut]
    topics: list[TopicOut]
    action_items: list[MeetingActionItemOut]

    class Config:
        from_attributes = True
