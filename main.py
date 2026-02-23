from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import settings
from skills.toggl_skill import TogglSkill

app = FastAPI(
    title="AI Productivity Orchestrator",
    description="Backend server for orchestrating AI productivity tasks",
    version="1.0.0"
)

class TimerRequest(BaseModel):
    task_name: str
    duration_minutes: Optional[int] = None
    workspace_id: str

class SlackNotificationRequest(BaseModel):
    message: str
    channel: Optional[str] = None

class AIProcessRequest(BaseModel):
    text: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.app_env}

@app.post("/start-timer")
async def start_timer(request: TimerRequest):
    toggl_skill = TogglSkill()
    duration_seconds = (request.duration_minutes * 60) if request.duration_minutes else -1
    
    result = toggl_skill.start_timer(
        description=request.task_name,
        duration=duration_seconds,
        workspace_id=request.workspace_id
    )
    
    if result.get("success"):
        return {"status": "success", "message": f"Timer started for '{request.task_name}'", "data": result.get("data")}
    raise HTTPException(status_code=400, detail=f"Failed to start timer: {result.get('error')}")

from skills.slack_skill import SlackSkill

@app.post("/slack-notify")
async def slack_notify(request: SlackNotificationRequest):
    slack_skill = SlackSkill()
    target_channel = request.channel if request.channel else "#general"
    
    result = slack_skill.send_slack_message(
        channel=target_channel,
        message=request.message
    )
    
    if result.get("success"):
        return {"status": "success", "message": f"Notification sent to {target_channel}"}
    raise HTTPException(status_code=400, detail=f"Failed to send Slack message: {result.get('error')}")

from skills.ai_router import AIRouter

@app.post("/ai-process")
async def ai_process(request: AIProcessRequest):
    router = AIRouter()
    result = router.process_text(request.text)
    
    return {
        "model_used": result["model_used"],
        "response": result["response"]
    }

from skills.email_skill import EmailSkill

class EmailRequest(BaseModel):
    to_address: str
    subject: str
    body: str

@app.post("/send-email")
async def send_email(request: EmailRequest):
    email_skill = EmailSkill()
    result = email_skill.send_email(request.to_address, request.subject, request.body)
    
    if result.get("success"):
        return {"status": "success", "message": result.get("message")}
    raise HTTPException(status_code=400, detail=f"Failed to send email: {result.get('error')}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
