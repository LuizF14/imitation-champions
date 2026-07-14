from dataclasses import dataclass

from agents.conversational_agent import ConversationalAgent
from agents.text_humanizer import TextHumanizer
from services.persona_service import pick_random_persona

@dataclass
class ConversationTurnResult:
    messages: list[str]

class ConversationService:
    def __init__(self):
        persona = pick_random_persona()
        self.main_agent = ConversationalAgent(persona)
        self.humanizer = TextHumanizer()

    def execute(self, user_message: str, thread_id: str) -> ConversationTurnResult:
        raw_answer = self.main_agent.run(user_message, thread_id)
        parts = self.humanizer.run(raw_answer)
        return ConversationTurnResult(messages=parts)