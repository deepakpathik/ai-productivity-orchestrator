from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_port: int = 8000
    
    toggl_api_key: Optional[str] = None
    slack_bot_token: Optional[str] = None
    gemini_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
