from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"

    provider_main_agent: str = "groq"
    provider_humanizer: str = "groq"
    provider_persona_generator: str = "groq"
    provider_judge: str = "groq"
    provider_interrogator: str = "groq"

    model_main_agent: str = "llama-3.3-70b-versatile"
    model_humanizer: str = "llama-3.1-8b-instant"
    model_persona_generator: str = "llama-3.1-8b-instant"
    model_judge: str = "llama-3.3-70b-versatile"
    model_interrogator: str = "llama-3.3-70b-versatile"

    groq_api_key: str = ""
    imitation_api_key: str = ""
    host: str = "http://localhost"
    port: str = "5000"
    backend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()


def get_chat_model(role: str, temperature: float = 0.7):
    provider = getattr(settings, f"provider_{role}")
    model = getattr(settings, f"model_{role}")

    if provider == "groq":
        from providers.groq_provider import get_groq_model
        return get_groq_model(model, temperature)
    elif provider == "ollama":
        from providers.ollama_provider import get_ollama_model
        return get_ollama_model(model, temperature)

    raise ValueError(f"Unknown provider: {provider}")