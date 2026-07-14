from config import get_chat_model
from schemas.judge_verdict import JudgeVerdict
from prompts.judge_prompt import JUDGE_PROMPT


class JudgeAgent:
    def __init__(self):
        llm = get_chat_model("judge", temperature=0)
        self._structured_llm = llm.with_structured_output(JudgeVerdict)

    def run(self, transcript: str) -> JudgeVerdict:
        return self._structured_llm.invoke(JUDGE_PROMPT.format(transcript=transcript))