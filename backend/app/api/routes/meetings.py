from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import ActionItem, Decision, Meeting, Topic, Transcript
from app.schemas.meeting import MeetingCreate, MeetingDetailOut, MeetingOut, MeetingUpdate
from app.services.analysis import extract_chunk, merge_structured_outputs, split_transcript_token_safe

router = APIRouter()


@router.get("", response_model=list[MeetingOut])
def list_meetings(db: Session = Depends(get_db)):
    return db.query(Meeting).order_by(Meeting.created_at.desc()).limit(100).all()


@router.post("", response_model=MeetingOut)
def create_meeting(payload: MeetingCreate, db: Session = Depends(get_db)):
    meeting = Meeting(source_type=payload.source_type, title=payload.title)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get("/{meeting_id}", response_model=MeetingOut)
def get_meeting(meeting_id: UUID, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.get("/{meeting_id}/detail", response_model=MeetingDetailOut)
def get_meeting_detail(meeting_id: UUID, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    transcript = db.query(Transcript).filter(Transcript.meeting_id == meeting_id).first()
    decisions = db.query(Decision).filter(Decision.meeting_id == meeting_id).all()
    topics = db.query(Topic).filter(Topic.meeting_id == meeting_id).all()
    action_items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()

    return {
        "id": meeting.id,
        "title": meeting.title,
        "status": meeting.status,
        "summary_text": meeting.summary_text,
        "transcript": transcript.full_text if transcript else None,
        "decisions": decisions,
        "topics": topics,
        "action_items": action_items,
    }


@router.patch("/{meeting_id}", response_model=MeetingOut)
def update_meeting(meeting_id: UUID, payload: MeetingUpdate, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(meeting, field, value)

    db.commit()
    db.refresh(meeting)
    return meeting


@router.post("/{meeting_id}/reprocess")
def reprocess_meeting(meeting_id: UUID, style: str = "shorter", db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    transcript = db.query(Transcript).filter(Transcript.meeting_id == meeting_id).first()
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript missing")

    chunks = split_transcript_token_safe(transcript.full_text)
    partials = [extract_chunk(c) for c in chunks]
    merged = merge_structured_outputs(partials)

    if style == "only_action_items":
        meeting.summary_text = "Action items only view generated."
    elif style == "more_formal":
        meeting.summary_text = f"Formal summary: {merged.summary}"
    else:
        meeting.summary_text = merged.summary[:500]

    db.query(Decision).filter(Decision.meeting_id == meeting_id).delete()
    for text in merged.decisions:
        db.add(Decision(meeting_id=meeting_id, text=text))

    db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).delete()
    for item in merged.action_items:
        db.add(
            ActionItem(
                meeting_id=meeting_id,
                task_text=item.get("task", ""),
                owner_name_raw=item.get("owner") or "Unassigned",
            )
        )

    db.query(Topic).filter(Topic.meeting_id == meeting_id).delete()
    for topic in merged.topics:
        db.add(Topic(meeting_id=meeting_id, name=topic))

    db.commit()
    return {"message": "Reprocessed without retranscription", "style": style}
