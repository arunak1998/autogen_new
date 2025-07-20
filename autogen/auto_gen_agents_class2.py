from dotenv import load_dotenv
import os
load_dotenv()
import asyncio
from typing_extensions import Annotated

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.http import HttpTool
api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the api key in evironemnt Varibale")
openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=api_key,
)
'''
fact": "A group of cats is called a clowder.",
  "length": 36
'''

json_schema={

  "title": "Cat Fact Schema",
  "type": "object",
  "properties": {
    "fact": {
      "type": "string",
      "description": "A fun fact about cats"
    },
    "length": {
      "type": "integer",
      "description": "The length of the fact string"
    }
  },
  "required": ["fact", "length"],

}

http_tool = HttpTool(
    name="Cat_facts_api",
    description="ge a cool cat fact",
    scheme="https",
    host="catfact.ninja",
    port=443,
    path="/fact",
    method="GET",
    json_schema=json_schema,
)

agent = AssistantAgent(
name="CatFactAgent",
model_client=openai_model_client,
tools=[http_tool],
reflect_on_tool_use=True, # your @tool-decorated function
system_message=(
    "You're CatFactAgent 🐾 — a chill, smart assistant who fetches fun, quirky cat facts. "
    "Use the `cat_gact_agent_api` tool to pull random cat facts when asked. "
    "Keep responses short, fun, and informative. "
 "If someone asks for a fact, don’t make stuff up — always call the tool."
)
)


async def main():
    result=await agent.run(task='Give a fun fact about cat"')

    print(result)


if __name__=="__main__":

    asyncio.run(main())