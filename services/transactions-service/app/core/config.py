# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    MODEL_PATH: str = "ml/model.joblib"

    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

settings = Settings()
