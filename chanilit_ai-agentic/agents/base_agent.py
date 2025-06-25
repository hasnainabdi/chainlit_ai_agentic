from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions
        
    @abstractmethod
    async def process_input(self, input_data: Dict[str, Any]) -> str:
        """Process input data and return response"""
        pass
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return True
