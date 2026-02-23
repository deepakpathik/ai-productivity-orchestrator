# AI Productivity Orchestrator

A backend server built with FastAPI for orchestrating AI productivity tasks.

## Features
- **FastAPI Backend:** Fast, robust, and asynchronous API server.
- **Skills:** Modular skills for Toggl, Slack, and Email integration.
- **Services:** Placeholder structure for Gemini and Claude language models.
- **AI Router:** Simple routing logic to direct instructions to appropriate skills or services.
- **Modular and Clean Structure:** Ready to be extended.

## Project Structure
```text
ai-productivity-orchestrator/
├── main.py              # FastAPI application entry point
├── config.py            # Environment configuration parser
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── utils/
│   └── logger.py        # Configured logger
├── services/
│   ├── gemini_service.py # Gemini AI integration
│   └── claude_service.py # Claude AI integration
└── skills/
    ├── toggl_skill.py   # Toggl timer skill
    ├── slack_skill.py   # Slack notification skill
    ├── email_skill.py   # Email sending skill
    └── ai_router.py     # Router for parsing and directing requests
```

## Setup & Run

1. **Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

4. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **API Documentation:**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) to access the interactive Swagger UI and test the API endpoints.

## API Endpoints

- `GET /health` - Check health status
- `POST /start-timer` - Start a timer via Toggl skill
- `POST /slack-notify` - Send a message via Slack skill
- `POST /ai-process` - Process a natural language instruction via AI Router
- `POST /send-email` - Send an email via SMTP
- `POST /whatsapp-webhook` - Twilio-compatible WhatsApp webhook to execute Smart Productivity Automation or query AI Router

## Set Up WhatsApp/Twilio Webhook (Optional)

1. **Start ngrok** to expose your local server to the internet:
   ```bash
   ngrok http 8000
   ```
2. **Copy the Forwarding URL** from ngrok (e.g., `https://abcd1234.ngrok-free.app`).
3. **Configure Twilio:**
   - In your Twilio WhatsApp Sandbox, locate the "WHEN A MESSAGE COMES IN" field.
   - Paste `[YOUR_NGROK_URL]/whatsapp-webhook`.
   - Save the configuration.
4. **Environment Variables:** Provide `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_WHATSAPP_NUMBER` in your `.env`.
5. Send a WhatsApp message to your Twilio number:
   - Example 1: `Plan my day` (routes to Claude/Gemini)
   - Example 2: `start 2 hour deep work` (routes to Toggl and Slack, bypassing AI)
