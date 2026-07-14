from langchain_ollama import ChatOllama

def get_ollama_model(model: str, temperature: float = 0.7):
    return ChatOllama(model=model, temperature=temperature)