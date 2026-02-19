from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "User Management API"
    environment: str = Field(default="local", description="local|dev|staging|prod")
    log_level: str = Field(default="INFO", description="DEBUG|INFO|WARNING|ERROR")

    # Use Postgres in prod (e.g. Cloud SQL), SQLite ok for local/tests
    database_url: str = Field(default="sqlite:///./local.db")

    # Cloud Run port
    port: int = 8080

settings = Settings()
