from pydantic import BaseModel, Field
from typing import Literal

class JudgeVerdict(BaseModel):
    evidence: list[str] = Field(
        description="lista de observações específicas da conversa que embasam o veredito, citando trechos"
    )
    verdict: Literal["humano", "ia"]
    confidence: int = Field(ge=0, le=100)
    reason: str = Field(description="resumo curto (1-2 frases) do principal fator que decidiu o veredito")