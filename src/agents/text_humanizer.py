from config import get_chat_model
from schemas.conversation import MessageChunks
from prompts.humanizer_prompt import SPLIT_PROMPT

class TextHumanizer:
    def __init__(self):
        llm = get_chat_model("humanizer", temperature=0.7)
        self._structured_llm = llm.with_structured_output(MessageChunks)

    def run(self, answer: str) -> list[str]:
        if len(answer) < 40:
            return [answer]
        result = self._structured_llm.invoke(SPLIT_PROMPT.format(answer=answer))
        return result.messages