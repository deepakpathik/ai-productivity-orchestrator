from services.gemini_service import GeminiService
from skills.toggl_skill import TogglSkill
from skills.slack_skill import SlackSkill
from skills.email_skill import EmailSkill

class AIRouter:
    def __init__(self):
        self.gemini = GeminiService()
        self.toggl = TogglSkill()
        self.slack = SlackSkill()
        self.email = EmailSkill()

    def process_text(self, text: str) -> dict[str, str]:
        model_used = "Gemini (LangChain)"
        response = self.gemini.generate_response(text)
            
        return {
            "model_used": model_used,
            "response": response
        }
