"""
Gemini service
Responsible for communicating with the Gemini API
"""

from google import genai
from config import Config

class GeminiService:
    """
    Wrapper around Google's Gemini API
    """

    def __init__(self):
        Config.validate()
        # Create Gemini Client
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_response(self, prompt: str)-> str:
        """
        Send Prompt to Gemini and return response
        Args:
            prompt: Complete prompt to send
        Returns:
            AI generated response
        """

        try:
            response = self.client.models.generate_content(
                model = Config.MODEL_NAME,
                prompt = prompt
            )
            return response.text
        except Exception as ex:
            raise RuntimeError(
                f"Gemini API Error : {ex}"
            )
