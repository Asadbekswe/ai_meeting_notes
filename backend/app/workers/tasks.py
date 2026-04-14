from app.db.session import SessionLocal
from app.models.entities import ActionItem, Decision, Meeting, MeetingStatus, Topic, Transcript
from app.services.analysis import extract_chunk, merge_structured_outputs, split_transcript_token_safe
from app.workers.celery_app import celery_app


def _fake_transcription_from_update(update: dict) -> str:
    message = update.get("message", {})
    if "text" in message:
        return message["text"]
    return "This is a placeholder transcript. Replace with Whisper transcription in production."


@celery_app.task(name="app.workers.tasks.process_meeting")
def process_meeting(update: dict):
    db = SessionLocal()
    try:
        meeting = Meeting(source_type="audio_file", status=MeetingStatus.received)
        db.add(meeting)
        db.commit()
        db.refresh(meeting)

        meeting.status = MeetingStatus.transcribing
        db.commit()

        transcript_text = _fake_transcription_from_update(update)
        transcript = Transcript(
            meeting_id=meeting.id,
            full_text=transcript_text,
            token_count=len(transcript_text.split()),
            model_name="whisper-placeholder",
        )
        db.add(transcript)
        db.commit()

        meeting.status = MeetingStatus.analyzing
        db.commit()

        chunks = split_transcript_token_safe(transcript_text)
        partials = [extract_chunk(c) for c in chunks]
        merged = merge_structured_outputs(partials)

        meeting.status = MeetingStatus.finalizing
        meeting.summary_text = merged.summary

        for text in merged.decisions:
            db.add(Decision(meeting_id=meeting.id, text=text))

        for item in merged.action_items:
            db.add(
                ActionItem(
                    meeting_id=meeting.id,
                    task_text=item.get("task", ""),
                    owner_name_raw=item.get("owner") or "Unassigned",
                )
            )

        for topic in merged.topics:
            db.add(Topic(meeting_id=meeting.id, name=topic))

        meeting.status = MeetingStatus.completed
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.send_reminders")
def send_reminders():
    db = SessionLocal()
    try:
        items = db.query(ActionItem).filter(ActionItem.reminder_enabled.is_(True)).all()
        # Placeholder for Telegram reminder delivery.
        return {"reminders_checked": len(items)}
    finally:
        db.close()
