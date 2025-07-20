from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


async def main():

    local=LocalCommandLineCodeExecutor(work_dir='/tmp',timeout=120)

    code_executor_agent=CodeExecutorAgent(name='CodeExecutorAgent',code_executor=local)

    task = TextMessage(
        content="""this is the code

    ```python
    print('hello world')```
    """,
    source="user"
    )




    await local.start()
    result=await code_executor_agent.on_messages(messages=[task],cancellation_token=CancellationToken)

    print(f'the result is {result}')


if __name__=='__main__':

    asyncio.run(main())