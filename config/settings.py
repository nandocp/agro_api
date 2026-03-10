from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # App stuff
    FASTAPI_ENV: str = 'DEVELOPMENT'
    DEBUG: bool | None = True

    # API
    API_PATH: str = '/api/v1'
    PROJECT_NAME: str = 'AgroAPI'
    VERSION: str = '0.2.0'

    # Database
    DATABASE_URL: str = (
        'postgresql+psycopg://api_user:Agr0_420@db:5432/agro_db'
    )

    # Security
    SECRET_KEY: str = (
        '076cf379f99ac223aead2e9e03e1b90466e03e8a3f0ec58e983d52589be70f22'
    )
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: List[str] = ['http://localhost:3000']

    LOG_LEVEL: str = 'DEBUG'


settings = Settings()
