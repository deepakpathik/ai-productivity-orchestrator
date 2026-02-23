import base64
import requests
from typing import Any
from datetime import datetime, timezone
from config import settings

class TogglSkill:
    def __init__(self):
        self.api_key = settings.toggl_api_key
        self.base_url = "https://api.track.toggl.com/api/v9"

    def _get_headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ValueError("TOGGL_API_KEY is missing configuration.")
        
        auth_string = f"{self.api_key}:api_token"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }

    def start_timer(self, description: str, duration: int, workspace_id: str) -> dict[str, Any]:
        if not self.api_key:
            return {"error": "TOGGL_API_KEY not configured", "success": False}

        url = f"{self.base_url}/workspaces/{workspace_id}/time_entries"
        
        payload = {
            "description": description,
            "duration": duration,
            "start": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "workspace_id": int(workspace_id),
            "created_with": "ai-productivity-orchestrator"
        }

        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            return {
                "success": True, 
                "data": response.json()
            }
        except requests.exceptions.RequestException as e:
            error_details = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.text
                except Exception:
                    pass
            return {
                "success": False, 
                "error": str(e),
                "details": error_details
            }

