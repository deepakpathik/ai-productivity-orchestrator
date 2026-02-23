from typing import Optional
from config import settings

class ClaudeService:
    def __init__(self):
        self.api_key = settings.claude_api_key

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        return f"Claude response for: {prompt}"
