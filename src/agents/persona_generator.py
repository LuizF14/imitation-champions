from services.persona_service import generate_personas, save_personas

class PersonaGeneratorAgent:
    def run(self, n: int = 20) -> int:
        personas = generate_personas(n)
        save_personas(personas)
        return len(personas)