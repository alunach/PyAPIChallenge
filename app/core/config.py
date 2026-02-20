from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    app_name: str = "user-api"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./app.db"

settings = Settings()
