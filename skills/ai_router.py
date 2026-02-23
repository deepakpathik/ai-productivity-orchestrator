from services.gemini_service import GeminiService
from services.claude_service import ClaudeService
from skills.toggl_skill import TogglSkill
from skills.slack_skill import SlackSkill
from skills.email_skill import EmailSkill

class AIRouter:
    def __init__(self):
        self.gemini = GeminiService()
        self.claude = ClaudeService()
        self.toggl = TogglSkill()
        self.slack = SlackSkill()
        self.email = EmailSkill()

    def process_text(self, text: str) -> dict[str, str]:
        word_count = len(text.split())
        
        if word_count > 500:
            model_used = "Claude"
            response = self.claude.generate_response(text)
        else:
            model_used = "Gemini"
            response = self.gemini.generate_response(text)
            
        return {
            "model_used": model_used,
            "response": response
        }
