from dotenv import load_dotenv
import os
load_dotenv()
import asyncio
from typing_extensions import Annotated
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the api key in evironemnt Varibale")
openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-2024-08-06",
    api_key=api_key,
)

def reverse_string(
    text: Annotated[str, "The string you want to reverse"]
) -> str:
    """
    Reverses the input string and returns it.

    Example:
    >>> reverse_string("hello")
    'olleh'
    """
    return text[::-1]

reverse_tool=FunctionTool(reverse_string,description="A tool to reverse a String")
agent = AssistantAgent(
    name="ReverseStringAgent",
    model_client=openai_model_client,
    tools=[reverse_string],
     reflect_on_tool_use=True, # your @tool-decorated function
    system_message=(
        "You are a utility assistant that reverses strings on request. "
        "Use the provided tool `reverse_string` to reverse any input string."
    )
)

async def main():
    result=await agent.run(task='Reverse the String "Hello World!"')

    print(result)

if __name__=="__main__":
     asyncio.run(main())