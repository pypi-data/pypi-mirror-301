from datetime import datetime

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate

from mtmai.agents.ctx import mtmai_context


class Assistant:
    async def stream_messages(self, messages: list[BaseMessage]):
        # memory = MemorySaver()
        assistant_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful customer support assistant for Website Helper, assisting users in using this system and answering user questions. "
                    "delegate the task to the appropriate specialized assistant by invoking the corresponding tool. You are not able to make these types of changes yourself."
                    " Only the specialized assistants are given permission to do this for the user."
                    "The user is not aware of the different specialized assistants, so do not mention them; just quietly delegate through function calls. "
                    "Provide detailed information to the customer, and always double-check the database before concluding that information is unavailable. "
                    " When searching, be persistent. Expand your query bounds if the first search returns no results. "
                    " If a search comes up empty, expand your search before giving up."
                    "\n 必须使用中文回复用户"
                    "\nCurrent time: {time}."
                    "{additional_instructions}",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())

        messages2 = assistant_prompt.format_messages(messages=messages)
        agent_executor = await mtmai_context.create_agent_excutor()
        config = {"configurable": {"thread_id": "abc123"}}
        for chunk in agent_executor.stream(messages2, config):
            if chunk.content:
                yield chunk.content
