from functools import lru_cache
from typing import List

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field("ConvocaFinder API", alias="APP_NAME")
    environment: str = Field("development", alias="ENVIRONMENT")
    database_url: str = Field(
        "postgresql+psycopg2://convoca:convoca@db:5432/convocafinder",
        alias="DATABASE_URL",
    )
    secret_key: str = Field("super-secret-dev-key", alias="SECRET_KEY")
    access_token_expire_minutes: int = 60 * 24
    smtp_host: str = Field("mailhog", alias="SMTP_HOST")
    smtp_port: int = Field(1025, alias="SMTP_PORT")
    smtp_username: str = Field("", alias="SMTP_USERNAME")
    smtp_password: str = Field("", alias="SMTP_PASSWORD")
    smtp_from_email: EmailStr = Field("convocafinder@example.com", alias="SMTP_FROM_EMAIL")
    telegram_bot_token: str = Field("", alias="TELEGRAM_BOT_TOKEN")
    telegram_channel_id: str = Field("", alias="TELEGRAM_CHANNEL_ID")
    sentry_dsn: str = Field("", alias="SENTRY_DSN")
    metrics_enabled: bool = Field(True, alias="METRICS_ENABLED")
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        alias="CORS_ORIGINS",
    )
    rate_limit_per_minute: int = Field(60, alias="RATE_LIMIT_PER_MINUTE")
    redis_url: str = Field("redis://redis:6379/0", alias="REDIS_URL")

    model_config = SettingsConfigDict(
        populate_by_name=True,
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
