from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    ENV: Literal["dev", "prod"] = "dev"
    TELEGRAM_TOKEN: str
    OPENROUTER_API_KEY: str

    # PostgreSQL
    POSTGRESQL_ENGINE: str = "postgresql"
    POSTGRESQL_DB: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int

    @property
    def DATABASE_URL(self):
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRESQL_USER,
            password=self.POSTGRESQL_PASSWORD,
            host=self.POSTGRESQL_HOST,
            port=self.POSTGRESQL_PORT,
            database=self.POSTGRESQL_DB
        )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
