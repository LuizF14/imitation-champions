from pydantic import BaseModel, Field
from typing import Literal

class JudgeVerdict(BaseModel):
    evidence: list[str] = Field(
        description="list of specific observations from the conversation that support the verdict, citing excerpts"
    )
    verdict: Literal["HUMAN", "AI"]
    reason: str = Field(description="A brief summary (1–2 sentences) of the main factor determining the verdict.")