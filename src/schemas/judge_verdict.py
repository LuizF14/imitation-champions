from pydantic import BaseModel, Field
from typing import Literal

class JudgeVerdict(BaseModel):
    verdict: Literal["HUMAN", "AI"]
    reason: str = Field(description="A brief summary (1–2 sentences) of the main factor determining the verdict.")