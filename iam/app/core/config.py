import secrets

from typing import Literal

from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn, EmailStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file='../../../.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    # Basic app configuration
    PROJECT_NAME: str = 'DeFi Dashboard IAM'
    API_VERSION_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'

    # Database configuration
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432

    TESTING: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        if self.TESTING:
            self.POSTGRES_DB = f'{self.POSTGRES_DB}-test'
            self.POSTGRES_SERVER = f'{self.POSTGRES_SERVER}-test'

        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

settings = Settings()
