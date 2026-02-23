from typing import Optional
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from twilio.rest import Client
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
    target_channel = request.channel if request.channel else settings.slack_default_channel
    
    result = slack_skill.send_slack_message(
        channel=target_channel,
        message=request.message
    )
    
    if result.get("success"):
        return {"status": "success", "message": f"Notification sent to {target_channel}"}
    raise HTTPException(status_code=400, detail=f"Failed to send Slack message: {result.get('error')}")

from services.gemini_service import GeminiService

SLACK_BOT_SYSTEM_PROMPT = """You are DeepakClaw, a smart and friendly AI productivity assistant built by Deepak Pathik. 
You live inside a Slack workspace and help team members with questions, brainstorming, coding help, and productivity tips.
You are NOT a generic AI model. You are DeepakClaw — a custom-built assistant integrated into Slack.
Keep your replies concise, helpful, and conversational. Use a professional but approachable tone.
If someone asks who you are, tell them you are DeepakClaw, built by Deepak Pathik as part of the AI Productivity Orchestrator project.
Never say you are trained by Google, OpenAI, or Anthropic. You are DeepakClaw."""

processed_events = set()

@app.post("/slack/events")
async def slack_events(request: Request):
    payload = await request.json()

    if payload.get("type") == "url_verification":
        return JSONResponse({"challenge": payload.get("challenge")})

    if payload.get("type") == "event_callback":
        event = payload.get("event", {})
        
        event_id = payload.get("event_id", "")
        if event_id in processed_events:
            return JSONResponse({"status": "duplicate"})
        processed_events.add(event_id)
        
        if event.get("bot_id") or event.get("subtype"):
            return JSONResponse({"status": "ignored"})
        
        if event.get("type") in ("app_mention", "message"):
            user_message = event.get("text", "")
            channel_id = event.get("channel")
            
            clean_message = user_message.split(">", 1)[-1].strip() if ">" in user_message else user_message
            
            gemini = GeminiService()
            ai_response = gemini.generate_response(clean_message, system_prompt=SLACK_BOT_SYSTEM_PROMPT)
            
            slack_skill = SlackSkill()
            slack_skill.send_slack_message(channel_id, ai_response)
            
    return JSONResponse({"status": "ok"})

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

from utils.logger import get_logger
logger = get_logger(__name__)


@app.post("/whatsapp-webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    user_message = Body

    if "start" in user_message.lower():
        toggl_skill = TogglSkill()
        slack_skill = SlackSkill()
        
        toggl_skill.start_timer("Deep Work", 7200, str(settings.toggl_workspace_id))
        
        slack_skill.send_slack_message(settings.slack_default_channel, f"🚀 Started 2 hours of Deep Work via WhatsApp! Task: {user_message}")
        
        ai_response = f"✅ Started deep work timer for 2 hours and notified Slack!\n\nOriginal request: {user_message}"
    else:
        router = AIRouter()
        result = router.process_text(user_message)
        ai_response = result["response"]

    if settings.twilio_account_sid and settings.twilio_auth_token:
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        try:
            client.messages.create(
                body=ai_response,
                from_=settings.twilio_whatsapp_number,
                to=From
            )
        except Exception as e:
            logger.error(f"Twilio error: {e}")

    return "OK"

from services.gemini_service import GeminiService

def daily_productivity_briefing() -> dict:
    slack = SlackSkill()
    slack_res = slack.send_slack_message(settings.slack_default_channel, "🌅 Good morning! Starting your daily briefing and activating deep work mode.")

    toggl = TogglSkill()
    toggl_res = toggl.start_timer("Deep Work - Morning Briefing", 7200, str(settings.toggl_workspace_id))

    gemini = GeminiService()
    ai_plan = gemini.generate_response("Give me a short, highly motivational 3-sentence productivity plan for the day.")

    return {
        "message": "Morning briefing executed successfully",
        "slack_status": slack_res,
        "deep_work_timer": toggl_res,
        "ai_plan": ai_plan
    }

@app.post("/morning-briefing")
async def morning_briefing():
    try:
        result = daily_productivity_briefing()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
