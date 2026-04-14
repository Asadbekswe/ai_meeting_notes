# AI Meeting Notes

Production-oriented system that converts Telegram meeting recordings into structured notes and syncs them to a collaboration dashboard.

## Product brief
AI Meeting Notes helps teams turn meetings into accountable execution. Users send voice notes, audio files, or transcripts in Telegram; the system transcribes and extracts summary, decisions, action items, and topics. Results are synced to a web dashboard with search, editing, and task tracking. This closes the gap between discussion and follow-through for daily business operations.

## Architecture
- Backend API: FastAPI (`backend/app`)
- Worker queue: Celery + Redis (`backend/app/workers`)
- Database: PostgreSQL (Docker compose)
- Storage: S3-compatible bucket (configured via env)
- Bot ingress: Telegram webhook endpoint (`/api/telegram/webhook`)
- Frontend: Next.js app router (`frontend/app`)
- Search: PostgreSQL full-text ready (indexes to add in migrations)

## Implemented scope
- Telegram webhook ingestion pipeline skeleton
- Meeting/transcript/action models
- Chunking + map/reduce analysis scaffolding
- Reprocess endpoint (style changes without re-transcription)
- Dashboard pages:
  - Home
  - Meetings list
  - Meeting detail
  - Action items (grouped by owner)
- Extra feature scaffold: automatic task reminders via worker task

## Repository structure
- `backend/` API, models, services, workers
- `frontend/` Next.js dashboard
- `infra/docker-compose.yml` PostgreSQL + Redis
- `scripts/` local run helpers

## Setup
### 1) Start infrastructure
```bash
cd infra
docker compose up -d
```

### 2) Backend
```bash
cd ../backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts_init_db.py
uvicorn app.main:app --reload --port 8000
```

### 3) Worker
```bash
cd backend
source .venv/bin/activate
celery -A app.workers.celery_app.celery_app worker -Q meetings,reminders --loglevel=info
```

### 4) Frontend
```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## Environment config
Backend `.env` keys:
- `DATABASE_URL`
- `REDIS_URL`
- `S3_BUCKET`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- `LLM_MODEL`
- `WHISPER_MODEL`

Frontend `.env.local` keys:
- `NEXT_PUBLIC_API_BASE`

## Telegram bot
- Webhook endpoint: `POST /api/telegram/webhook`
- Configure Telegram webhook to your deployed API URL and secret token.
- Bot username: set after BotFather creation (example: `@ai_meeting_notes_bot`).

## Real sample output format
```text
[Meeting Summary]
The team aligned on Q2 launch priorities, confirmed scope for onboarding improvements, and identified a risk around migration timing. They agreed to split rollout into two phases and publish a customer communication plan. Engineering and operations confirmed dependencies and target dates.

[Key Decisions]
• Launch in two phases instead of a single release.
• Keep legacy import path active for 30 days post-launch.

[Action Items]
• Draft customer migration email — Sara
• Finalize rollback checklist — Unassigned
• Prepare support runbook — Alex

[Topics]
• Q2 launch scope
• Migration risk
• Customer communications
• Support readiness
```

## Screen recording checklist
1. Upload audio in Telegram.
2. Show bot progress states: received, transcribing, analyzing, finalizing.
3. Show final structured note in Telegram.
4. Open dashboard and show new meeting/task sync.
5. Edit a task status inline in dashboard.

## Extra feature: automatic task reminders
What it does:
- Worker scans pending/in-progress tasks and sends Telegram reminders.

Why it matters:
- Converts meeting notes into execution by nudging owners where they already work.

## Next 3 days
Day 1: Replace placeholder transcription and extraction with real Whisper + LLM providers, add strict JSON schema validation, and implement robust error handling for unclear audio and ambiguous ownership. Day 2: add Alembic migrations, full-text search indexes, realtime event broadcasting, and inline edit APIs for decisions/topics/transcript. Day 3: production hardening with observability, retry/dead-letter policies, reminder scheduling, end-to-end tests, and deployment to cloud (API, worker, DB, Redis, frontend) with a live Telegram bot username.
