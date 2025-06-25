from .base_agent import BaseAgent
from aipro import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

class FrontendAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Frontend Expert",
            instructions="You are a frontend expert specializing in modern web development."
        )
        
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        self.external_client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=self.external_client
        )
        
        self.config = RunConfig(
            model=self.model,
            model_provider=self.external_client,
            tracing_disabled=True
        )
        
        self.agent = Agent(
            name=self.name,
            instructions=self.instructions
        )
        
    async def process_input(self, input_data: Dict[str, Any]) -> str:
        """Process input data using Gemini API"""
        try:
            result = await Agent.run_async(
                self.agent,
                input=input_data.get("message", ""),
                run_config=self.config
            )
            return result.final_output
        except Exception as e:
            return f"Error processing request: {str(e)}"
