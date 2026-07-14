from pydantic import BaseModel, Field
from typing import Literal

class Persona(BaseModel):
    id: str = Field(description="slug único, ex: 'marcos-bh-27'")
    name: str
    age: int = Field(ge=18, le=70)
    city: str
    state: str
    profession: str
    gender: Literal["masculino", "feminino"]
    personality_traces: list[str] = Field(
        description="3 a 5 traços, ex: ['sarcástico', 'impaciente', 'curioso']"
    )
    interests: list[str] = Field(description="2 a 4 interesses/hobbies")
    writing_style: str = Field(
        description="descrição curta de tique de escrita, ex: 'usa muito \"mano\", nunca usa vírgula'"
    )
    frequent_slang: list[str] = Field(default_factory=list)
    personal_context: str = Field(
        description="1-2 frases de background que podem surgir na conversa, ex: 'mora sozinho, tem um gato'"
    )

class PersonaBatch(BaseModel):
    personas: list[Persona]