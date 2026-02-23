import os
from config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class GeminiService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = None
        if self.api_key:
            os.environ["GOOGLE_API_KEY"] = self.api_key
            self.model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7,
                max_output_tokens=1024
            )

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        if not self.api_key or not self.model:
            return "Please provide a valid GEMINI_API_KEY in the `.env` file to unlock AI responses."

        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error interacting with Gemini API via LangChain: {str(e)}"
