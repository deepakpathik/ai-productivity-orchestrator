from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_port: int = 8000
    
    toggl_api_token: Optional[str] = None
    toggl_workspace_id: Optional[str] = None
    slack_bot_token: Optional[str] = None
    slack_default_channel: str = "#test-bot"
    gemini_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None
    
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None

    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatsapp_number: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
