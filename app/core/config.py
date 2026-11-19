
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "RAG Knowledge Base"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str

    QDRANT_URL: str = "https://ac4678ef-4c0a-45a2-8707-3e56494b03e7.us-east-2-0.aws.cloud.qdrant.io"
    QDRANT_API_KEY: str | None = None

    GEMINI_API_KEY: str | None = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
