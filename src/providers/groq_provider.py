from config import settings
from langchain_groq import ChatGroq

def get_groq_model(model: str, temperature: float = 0.7):
    return ChatGroq(model=model, temperature=temperature, api_key=settings.groq_api_key)