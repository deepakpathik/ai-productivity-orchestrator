from services.gemini_service import GeminiService
from services.claude_service import ClaudeService
from skills.toggl_skill import TogglSkill
from skills.slack_skill import SlackSkill
from skills.email_skill import EmailSkill
from utils.logger import get_logger

logger = get_logger(__name__)

class AIRouter:
    def __init__(self):
        self.gemini = GeminiService()
        self.claude = ClaudeService()
        self.toggl = TogglSkill()
        self.slack = SlackSkill()
        self.email = EmailSkill()

    def route_instruction(self, instruction: str, context: str | None = None) -> str:
        """
        Determine which service/skill should handle the instruction.
        This is a rudimentary implementation logic.
        """
        logger.info(f"Routing instruction: {instruction[:50]}...")
        
        lower_instruction = instruction.lower()
        if "time" in lower_instruction or "start" in lower_instruction:
            self.toggl.start_timer(instruction)
            return "Routed to Toggl to start timer."
        elif "slack" in lower_instruction or "message" in lower_instruction:
            self.slack.send_message(instruction)
            return "Routed to Slack to send message."
        elif "email" in lower_instruction:
             self.email.send_email("user@example.com", "Task Update", instruction)
             return "Routed to Email to send email."
        else:
             response = self.gemini.generate_response(instruction, context)
             return f"Processed by AI: {response}"
