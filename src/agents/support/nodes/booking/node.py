from langchain.agents import create_agent
from agents.support.nodes.booking.tools import tools
from dotenv import load_dotenv

load_dotenv()

# from src.agents.booking.prompt import prompt_template

agent = create_agent(
    model="deepseek:deepseek-reasoner",
    tools=tools,
    system_prompt="Your are a helpul assistant",
)
