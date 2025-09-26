from functools import lru_cache
from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "ConvocaFinder API"
    environment: str = "development"
    database_url: str = Field("postgresql+psycopg2://convoca:convoca@db:5432/convocafinder", env="DATABASE_URL")
    secret_key: str = Field("super-secret-dev-key", env="SECRET_KEY")
    access_token_expire_minutes: int = 60 * 24
    smtp_host: str = Field("mailhog", env="SMTP_HOST")
    smtp_port: int = Field(1025, env="SMTP_PORT")
    smtp_username: str = Field("", env="SMTP_USERNAME")
    smtp_password: str = Field("", env="SMTP_PASSWORD")
    smtp_from_email: EmailStr = Field("convocafinder@example.com", env="SMTP_FROM_EMAIL")
    telegram_bot_token: str = Field("", env="TELEGRAM_BOT_TOKEN")
    telegram_channel_id: str = Field("", env="TELEGRAM_CHANNEL_ID")
    sentry_dsn: str = Field("", env="SENTRY_DSN")
    metrics_enabled: bool = Field(True, env="METRICS_ENABLED")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    rate_limit_per_minute: int = Field(60, env="RATE_LIMIT_PER_MINUTE")
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
