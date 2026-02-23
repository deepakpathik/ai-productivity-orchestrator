from typing import Optional
from config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.gemini_api_key

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        return f"Gemini response for: {prompt}"
