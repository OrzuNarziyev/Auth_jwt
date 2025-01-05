from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    db_uri: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    access_token_lifetime: timedelta = timedelta(hours=3)
    refresh_token_lifetime: timedelta = timedelta(days=7)


settings = Settings()
