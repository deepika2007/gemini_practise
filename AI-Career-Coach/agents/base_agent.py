"""
Base Agent

Every AI agent inherits from this class
"""

from abc import ABC, abstractmethod
from services.gemini_service import GeminiService
from memory.shared_memory import SharedMemory

class BaseAgent(ABC):
    """
    Abstract Base class for all AI agents
    """

    def __init__(self, memory:SharedMemory):
        super().__init__()
        self.memory = memory
        self.gemini = GeminiService()


    @abstractmethod
    def execute(self)-> str:
        """
        Execute agent
        """
        pass

    def ask_gemini(self, prompt:str) -> str:
        """
        Send prompt to gemini
        """

        return self.gemini.generate_response(prompt)

    