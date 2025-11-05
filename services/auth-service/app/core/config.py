"""
Global configuration file.
Loads environment variables from `.env` for database and JWT settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Database ---
    DATABASE_URL: str

    # --- JWT Authentication ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Internal service API key (optional, for microservices communication) ---
    INTERNAL_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore unexpected env vars to prevent crashes


# Global instance used across the app
settings = Settings()
