from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    INTERNAL_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()