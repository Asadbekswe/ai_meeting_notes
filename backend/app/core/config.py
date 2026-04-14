from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "AI Meeting Notes API"
    env: str = "dev"
    api_prefix: str = "/api"

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/meeting_notes"
    redis_url: str = "redis://localhost:6379/0"
    s3_bucket: str = "meeting-notes-audio"

    telegram_bot_token: str = ""
    telegram_webhook_secret: str = ""

    llm_model: str = "gpt-5.3-codex"
    whisper_model: str = "whisper-1"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


settings = Settings()
