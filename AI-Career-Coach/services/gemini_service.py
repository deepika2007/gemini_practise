"""
Gemini service
Responsible for communicating with the Gemini API

Responsibilities:
1. Initialize Gemini Client
2. Senf prompts to Gemini
3. Return the complete Gemini response
4. Keep API- sepcific code isolated from Agents
"""

from google import genai
from config import Config
from typing import Any, Optional

class GeminiService:
    """
    Wrapper around Google's Gemini API
    """

    def __init__(self):
        Config.validate()
        # Create Gemini Client
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_response(self, prompt: str, config: Optional[Any] = None) -> Any:
        """
        Send Prompt to Gemini and return response
        Args:
            prompt: Complete prompt to send
            config: Optional GenerateContentCOnfig
        Returns:
            AI generated response
        """

        try:
            response = self.client.models.generate_content(
                model = Config.MODEL_NAME,
                contents = prompt,
                config = config
            )
            return response
        except Exception as ex:
            raise RuntimeError(
                f"Gemini API Error : {ex}"
            )
