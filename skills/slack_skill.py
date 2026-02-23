from typing import Optional
from config import settings

class SlackSkill:
    def __init__(self):
        self.bot_token = settings.slack_bot_token

    def send_message(self, message: str, channel: Optional[str] = None) -> bool:
        return True
