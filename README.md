see
# AI Productivity Orchestrator

> **An autonomous, intelligent backend layer that bridges natural language tasks with real-world productivity tools.**

The **AI Productivity Orchestrator** is a robust FastAPI-based backend designed to streamline day-to-day work processes. By combining Large Language Models (LLMs) with common productivity APIs, it acts as a central hub for starting timers, sending notifications, summarizing workloads, and executing daily briefings—all via natural language or automated webhooks.

## Resume-Ready Description

**AI Productivity Orchestrator**
*Developed a scalable, asynchronous FastAPI application that orchestrates cross-platform productivity tasks using LLMs.*
* **Intelligent Routing**: Implemented dynamic context-based payload routing between Anthropic's Claude and Google's Gemini models for optimized cost and context handling.
* **Third-Party Integrations**: Engineered modular connections with the Slack Web API, Toggl Track REST API v9, Twilio WhatsApp Sandbox, and an SMTP Email Server.
* **Smart Automations**: Designed automated workflows, including a "Morning Briefing" protocol that triggers deep work timers, sends Slack broadcasts, and synthesizes motivational AI plans in a single sequence.
* **Architecture**: Built using a clean, extensible pattern separating `services` (LLMs), `skills` (third-party APIs), and application logic.

## Architecture Overview

The project is built on **FastAPI** to benefit from native asynchronous endpoints, Python type hints, and automatic API documentation (Swagger UI). 

The codebase separates concerns logically into:
* **`services/`**: Wrappers for the core artificial intelligence models (Claude 3 Haiku, Gemini 1.5 Flash).
* **`skills/`**: Encapsulated modules that execute actions on third-party platforms (Email, Slack, Toggl).
* **Routing logic (`AI Router`)**: A middleware controller that evaluates user prompt complexity (via word count) to determine the most efficient LLM.

## Integrated Services

1. **Slack**: Broadcasts notifications to designated channels using the official `slack_sdk`.
2. **Toggl Track**: Initiates time entries for specific workspaces via direct HTTP calls to the Toggl REST API v9.
3. **Google Gemini (1.5 Flash)**: Optimized for fast, concise responses to short prompts.
4. **Anthropic Claude (3 Haiku)**: Used for handling larger context windows and more complex reasoning tasks.
5. **Email (SMTP)**: Handles outbound structured email delivery using Python's native `smtplib`.
6. **WhatsApp (Twilio)**: Exposes a webhook to receive inbound WhatsApp messages, process them through the AI router, and reply natively via Twilio's messaging API.

## How AI Routing Works

The `AIRouter` is a dynamic dependency that inspects incoming text requests. 
- For prompts under **500 words**, the router favors execution speed and cost-effectiveness by delegating the generation to **Gemini**. 
- For heavier payloads or prompts with extensive context exceeding **500 words**, the router forwards the request to **Claude**, leveraging its larger context window capabilities.

## How the Toggl REST API is Used

The Toggl integration leverages the **Toggl API v9**. It constructs authenticated HTTP requests using basic authentication, encoding the provided `TOGGL_API_KEY` combined with the standard `api_token` string. 
Upon receiving a request mapping a duration, workspace, and task description, it constructs the necessary JSON payload with localized ISO 8601 UTC timestamps, ensuring exact tracking within the user's Toggl dashboard.

---

## Screenshots

*(Replace these placeholders with your actual application screenshots)*

| Swagger API Docs | Twilio WhatsApp Integration |
|:---:|:---:|
| <img src="docs/placeholder-swagger.png" width="400" alt="Swagger UI" /> | <img src="docs/placeholder-whatsapp.png" width="400" alt="WhatsApp UI" /> |

| Slack Notifications | Toggl Timer Dashboard |
|:---:|:---:|
| <img src="docs/placeholder-slack.png" width="400" alt="Slack Notifications" /> | <img src="docs/placeholder-toggl.png" width="400" alt="Toggl Dashboard" /> |

---

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Twilio Account (for WhatsApp webhooks)
- Slack Bot Token (with `chat:write` scopes)
- Toggl Track API Token
- Gemini & Anthropic API Keys

### 2. Installation
Clone the repository and install dependencies in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Populate the file with your specific credentials and keys.

### 4. Running the Server
Launch the application locally using Uvicorn:
```bash
uvicorn main:app --reload
```

### 5. (Optional) Testing Webhooks Locally
Use ngrok to expose your local instance for Twilio:
```bash
ngrok http 8000
```
*Take the forwarding URL and place it in your Twilio Sandbox settings.*

---

## Demo API Endpoints

Once the server is running, navigate to `http://localhost:8000/docs` to test:

- `GET /health` 
  - Standard ping mechanism to verify server environment.
- `POST /start-timer`
  - Needs `task_name`, `workspace_id`, and `duration_minutes`. Validates directly against Toggl API.
- `POST /slack-notify`
  - Accepts `message` and `channel`. Sends payload to the Slack workspace.
- `POST /send-email`
  - Requires `to_address`, `subject`, and `body`. Uses secured standard SMTP delivery.
- `POST /ai-process`
  - Accepts raw text. Passes string through the `AIRouter` and returns the generated content and the underlying model used.
- `POST /whatsapp-webhook`
  - Twilio-compatible endpoint. Parses inbound WhatsApp messages. Automates direct toggl/slack actions if the `start` trigger is invoked.
- `POST /morning-briefing`
  - Executes a chained routine: Sends a Slack summary, starts a Toggl deep work timer, and formulates an AI-based motivational plan.
