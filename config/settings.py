from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # App stuff
    ENVIRONMENT: str = 'development'
    DEBUG: bool | None = True

    # API
    API_PATH: str = '/api/v1'
    PROJECT_NAME: str = 'AgroAPI'
    VERSION: str = '0.2.0'

    # Database
    DATABASE_URL: str = (
        'postgresql+psycopg://postgres:postgres@127.0.0.1:5432/agro_db'
    )

    TEST_DATABASE_URL: str = (
        'postgresql+psycopg://postgres:postgres@127.0.0.1:5432/agro_db_test'
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

    SUPERADMIN_EMAIL: str = 'user@system.br'
    SUPERADMIN_PASSWORD: str = 'password'

    MAX_FAILED_ATTEMPTS: int = 5

    @property
    def active_database_url(self) -> str:
        if self.ENVIRONMENT == 'test':
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL


settings = Settings()
