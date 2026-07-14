from config import get_chat_model
from prompts.interrogator_prompt import INTERROGATOR_PROMPT

class InterrogatorAgent:
    def __init__(self):
        self.llm = get_chat_model("interrogator", temperature=0.9)

    def run(self, transcript: str) -> str:
        history = transcript if transcript else "(início da conversa)"
        resposta = self.llm.invoke(
            INTERROGATOR_PROMPT.format(history=history)
        )
        return resposta.content.strip()