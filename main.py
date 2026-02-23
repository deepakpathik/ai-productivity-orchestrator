from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="AI Productivity Orchestrator",
    description="Backend server for orchestrating AI productivity tasks",
    version="1.0.0"
)

# Request Models
class TimerRequest(BaseModel):
    task_name: str
    duration_minutes: int | None = None

class SlackNotificationRequest(BaseModel):
    message: str
    channel: str | None = None

class AIProcessRequest(BaseModel):
    instruction: str
    context: str | None = None

@app.get("/health")
async def health_check():
    """Health check endpoint to verify server status."""
    logger.info("Health check requested")
    return {"status": "ok", "environment": settings.app_env}

@app.post("/start-timer")
async def start_timer(request: TimerRequest):
    """Start a productivity timer (e.g., Toggl)."""
    logger.info(f"Start timer requested for task: {request.task_name}")
    # TODO: Integrate with toggl_skill
    return {"status": "success", "message": f"Timer started for '{request.task_name}'"}

@app.post("/slack-notify")
async def slack_notify(request: SlackNotificationRequest):
    """Send a notification via Slack."""
    logger.info(f"Slack notification requested. Message length: {len(request.message)}")
    # TODO: Integrate with slack_skill
    return {"status": "success", "message": "Notification queued"}

@app.post("/ai-process")
async def ai_process(request: AIProcessRequest):
    """Process an instruction using AI."""
    logger.info(f"AI processing requested. Instruction: {request.instruction[:50]}...")
    # TODO: Integrate with ai_router
    return {"status": "success", "result": "AI processing complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
