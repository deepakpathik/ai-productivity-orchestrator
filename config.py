import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_port: int = 8000
    
    toggl_api_token: str | None = None
    slack_bot_token: str | None = None
    gemini_api_key: str | None = None
    claude_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
