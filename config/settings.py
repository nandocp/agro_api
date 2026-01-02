from typing import List

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # App stuff
    FASTAPI_ENV: str

    # API
    API_PATH: str
    PROJECT_NAME: str = 'AgroAPI'
    VERSION: str = '0.2.0'

    # Database
    DATABASE_URL: PostgresDsn

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS
    CORS_ORIGINS: List[str]


settings = Settings()
