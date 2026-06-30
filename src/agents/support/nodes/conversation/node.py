from langchain.agents import create_agent
from dotenv import load_dotenv

agent = create_agent(
    model = "deepseek:deepseek-reasoner",
    