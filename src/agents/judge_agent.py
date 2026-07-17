from config import get_chat_model
from schemas.judge_verdict import JudgeVerdict
from prompts.judge_prompt import JUDGE_PROMPT

import re
from schemas.judge_verdict import JudgeVerdict

class JudgeAgent:
    def __init__(self):
        self._llm = get_chat_model("judge", temperature=0)

    def run(self, transcript: str) -> JudgeVerdict:
        prompt = JUDGE_PROMPT.format(transcript=transcript)
        response = self._llm.invoke(prompt)
        return self._parse_verdict(response.content)

    def _parse_verdict(self, text: str) -> JudgeVerdict:
        verdict_match = re.search(r"Verdict:\s*(\w+)", text, re.IGNORECASE)
        reason_match = re.search(r"Reason:\s*(.+)", text, re.IGNORECASE | re.DOTALL)

        if not verdict_match or not reason_match:
            raise ValueError(f"Formato de saída inesperado do juiz: {text!r}")

        return JudgeVerdict(
            verdict=verdict_match.group(1).strip(),
            reason=reason_match.group(1).strip(),
        )