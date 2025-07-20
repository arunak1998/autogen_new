import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
from typing_extensions import Annotated
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from langchain_community.utilities import GoogleSerperAPIWrapper
api_key=os.getenv("OPENAI_API_KEY")

serp_api_key=os.getenv("SERPER_API")
os.environ["SERPER_API_KEY"] = serp_api_key
if not api_key:
    raise ValueError("Please set the api key in evironemnt Varibale")
openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=api_key,
)
google_serper = GoogleSerperAPIWrapper(type='news')
def search_tool(query)->str:

    """ Search the Web for Given query and return Result"""

    try:

        result=google_serper.run(query)


        return result
    except Exception as e:
        print(f"Error occured while searchign the web {e}")

        return f"no results Found"

agent = AssistantAgent(
name="SearchThe Web",
model_client=openai_model_client,
tools=[search_tool],
reflect_on_tool_use=True, # your @tool-decorated function
system_message=(
    "You're a helpful AI assistant with access to real-time web search. "
    "Use the `search` tool to look up accurate and up-to-date information when answering questions. "
    "Don’t rely on memory — always search when the answer isn’t certain or needs freshness. "
    "Keep your responses clear, concise, and grounded in the search results."
)
)

async def main():
    result = await agent.run("Who won the latest IPL?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

