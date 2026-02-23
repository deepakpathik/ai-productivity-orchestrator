from typing import Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import settings

class SlackSkill:
    def __init__(self):
        self.bot_token = settings.slack_bot_token
        self.client = WebClient(token=self.bot_token) if self.bot_token else None

    def send_slack_message(self, channel: str, message: str) -> dict[str, Any]:
        if not self.client:
            return {"error": "SLACK_BOT_TOKEN not configured", "success": False}

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message
            )
            return {"success": True, "data": response.data}
        except SlackApiError as e:
            error_msg = e.response["error"] if e.response else str(e)
            return {"success": False, "error": error_msg}

