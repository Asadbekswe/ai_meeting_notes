#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
celery -A app.workers.celery_app.celery_app worker -Q meetings,reminders --loglevel=info
