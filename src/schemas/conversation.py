from pydantic import BaseModel, Field

class MessageChunks(BaseModel):
    messages: list[str] = Field(
        description="A resposta quebrada em 1 a 4 mensagens curtas, como alguém digitaria no WhatsApp"
    )