from google import genai
from google.genai.types import GenerateContentConfig, Part
import os
import json
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.configure_client()
        self.generation_config= GenerateContentConfig(
                    temperature= self.config['llm']['temperature'], 
                    seed= self.config['llm']['seed'])
    
    def load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Config file not found. Please create config.json")
    
    def configure_client(self):
        """Configure Gemini client with API key"""
        load_dotenv()
        if not os.getenv('GEMINI_API_KEY'):
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        #client with retry strategy: https://geminibyexample.com/029-rate-limits-retries/,
        # https://discuss.ai.google.dev/t/gemini-types-httpretryoptions-error/107128
        self.client = genai.Client(
            http_options= genai.types.HttpOptions(
                retry_options= genai.types.HttpRetryOptions(
                    attempts= self.config['llm_client']['retry_attempts'], 
                    max_delay= self.config['llm_client']['max_delay'])
            )
        )
    
    def analyze_text(self, prompt: str, text: str) -> str:
        """Analyze text using Gemini Pro"""
        try:
            response = self.client.models.generate_content(
                model = self.config['llm']['model_name'], 
                contents = f"{prompt}\n\nContent to analyze:\n{text}", 
                config = self.generation_config
                )
            return response.text
        except Exception as e:
            return f"Text Analysis Error: {str(e)}"
    
    def analyze_multimodal(self, prompt: str, image_bytes: bytes) -> str:
        """Analyze image using Gemini Pro Vision"""
        try:
            response = self.client.models.generate_content(
                model = self.config['llm']['model_name'],
                contents= [
                    prompt,
                    Part.from_bytes(
                        data= image_bytes,
                        mime_type= "image/png"),
                        ],
                config = self.generation_config
            )
            return response.text
        except Exception as e:
            return f"Vision Analysis Error: {str(e)}"