import anthropic
from config import settings

class ClaudeService:
    def __init__(self):
        self.api_key = settings.claude_api_key
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def generate_response(self, prompt: str) -> str:
        if not self.client:
            return "Error: CLAUDE_API_KEY is not configured."
        
        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error interacting with Claude API: {str(e)}"

