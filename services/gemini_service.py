import google.generativeai as genai
from config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_response(self, prompt: str) -> str:
        if not self.api_key:
            return "Please provide a valid GEMINI_API_KEY in the `.env` file to unlock AI responses."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "404 models" in str(e):
                return "Please provide a valid GEMINI_API_KEY in the `.env` file to unlock AI responses."
            return f"Error interacting with Gemini API: {str(e)}"
