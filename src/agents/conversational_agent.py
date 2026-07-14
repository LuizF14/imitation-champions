from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from config import get_chat_model
from schemas.persona import Persona
from prompts.conversation_prompt import build_prompt_from_persona
from tools.datetime_tools import get_current_date, get_current_datetime

class ConversationalAgent:
    def __init__(self, persona: Persona):
        self.persona = persona
        llm = get_chat_model("main_agent", temperature=0.9)
        self._agent = create_agent(
            model=llm,
            system_prompt=build_prompt_from_persona(persona),
            tools=[get_current_date, get_current_datetime],
            checkpointer=InMemorySaver(),
        )

    def run(self, mensagem: str, thread_id: str) -> str:
        resultado = self._agent.invoke(
            {"messages": [{"role": "user", "content": mensagem}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        return resultado["messages"][-1].content