import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file='../../../.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    API_VERSION_STR: str = '/api/v1'
    SECRET_KEY: str = secrets.token_urlsafe(32)

settings = Settings() 
