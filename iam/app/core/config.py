import secrets

from typing import Annotated, Any, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file='../../../.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    PROJECT_NAME: str = 'DeFi Dashboard IAM'
    API_VERSION_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'

settings = Settings()
