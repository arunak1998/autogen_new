from dotenv import load_dotenv
import os
load_dotenv()
import asyncio
from typing_extensions import Annotated
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the api key in evironemnt Varibale")
openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=api_key,
)


agent = AssistantAgent(
name="CatFactAgent",
model_client=openai_model_client,


)