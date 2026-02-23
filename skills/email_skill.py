import smtplib
from email.message import EmailMessage
from typing import Any
from config import settings

class EmailSkill:
    def __init__(self):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_password

    def send_email(self, to_address: str, subject: str, body: str) -> dict[str, Any]:
        if not self.user or not self.password:
            return {"success": False, "error": "SMTP credentials not configured"}

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = to_address

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            return {"success": True, "message": f"Email sent to {to_address}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
