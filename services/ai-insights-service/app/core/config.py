from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DB_URL: str = ""
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
