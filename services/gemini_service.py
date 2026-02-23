from typing import Optional
from typing import Any
import google.generativeai as genai
from config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt: str) -> str:
        if not self.api_key:
            return "Error: GEMINI_API_KEY is not configured."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error interacting with Gemini API: {str(e)}"

