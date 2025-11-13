"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Quillography Content Suite"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite:///./quillography.db"

    # AI Service
    openai_api_key: str = ""
    use_fake_ai: bool = True

    # Authentication
    api_key_enabled: bool = False
    api_key: str = "dev-api-key"

    # CORS
    cors_origins: List[str] = [
        "http://localhost:5000",
        "https://*.replit.dev",
        "*",
    ]

    # Server
    host: str = "0.0.0.0"
    # Port 8000 for development (when running alongside Vite dev server)
    # Port 5000 for production (serving both frontend and API)
    port: int = 8000

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() in ("production", "prod")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
