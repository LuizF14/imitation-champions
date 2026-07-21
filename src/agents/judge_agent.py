from config import get_chat_model
from schemas.judge_verdict import JudgeVerdict
from prompts.judge_prompt import JUDGE_PROMPT
from schemas.judge_verdict import JudgeVerdict

class JudgeAgent:
    def __init__(self):
        self._llm = get_chat_model("judge", temperature=0)
        self.classifier = get_chat_model("judge_classifier")

    def run(self, transcript: str) -> JudgeVerdict:
        verdict = self.classifier.classify(transcript)
        prompt = JUDGE_PROMPT.format(transcript=transcript, label=verdict)
        response = self._llm.invoke(prompt)
        return JudgeVerdict(verdict=verdict, reason=response.content)