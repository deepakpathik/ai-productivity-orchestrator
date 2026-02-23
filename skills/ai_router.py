from typing import Optional
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

    def route_instruction(self, instruction: str, context: Optional[str] = None) -> str:
        lower_instruction = instruction.lower()
        if "time" in lower_instruction or "start" in lower_instruction:
            workspace_id = context if context else "0000000"
            result = self.toggl.start_timer(instruction, -1, workspace_id)
            if result.get("success"):
                return f"Routed to Toggl and started timer: {result['data'].get('id')}."
            return f"Failed to start Toggl timer: {result.get('error')}"
        elif "slack" in lower_instruction or "message" in lower_instruction:
            self.slack.send_message(instruction)
            return "Routed to Slack to send message."
        elif "email" in lower_instruction:
            self.email.send_email("user@example.com", "Task Update", instruction)
            return "Routed to Email to send email."
        
        response = self.gemini.generate_response(instruction, context)
        return f"Processed by AI: {response}"
