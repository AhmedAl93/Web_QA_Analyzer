from browser_use import Agent, Browser, llm
from browser_use.agent.views import AgentHistoryList
import os, json
from dotenv import load_dotenv
load_dotenv()

class AgenticAnalyzer:
    def __init__(self, config_path):
        self.config= self.load_config(config_path)
        self.llm = llm.ChatGoogle(
			model= self.config["llm"]["model_name"],
            api_key= os.getenv("GEMINI_API_KEY"),
            temperature= self.config["llm"]["temperature"],
			max_retries= self.config["llm_client"]["retry_attempts"],
			retry_delay= self.config["llm_client"]["max_delay"],
            )
        self.browser = Browser()


    def load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    async def analyze(self, url: str) -> AgentHistoryList:
        """ 
        """
        agent = Agent(
            task = f"""
            You are a highly skilled Senior QA Agent. Load {url} and provide QA feedback:
            - UX: Is navigation intuitive? Any confusing layouts or slow interactions?
            - HTML Bugs: Check for broken images, invalid tags, console errors.
            - Extras: Accessibility score (e.g., alt texts), mobile-friendliness, load time.
            Be detailed but concise; output as bullet points with severity (low/medium/high).
            """,
            llm= self.llm,
            browser= self.browser,
        )

        history = await agent.run()
        return history
    
    

    