import json
import random
from pathlib import Path

from config import get_chat_model
from schemas.persona import Persona, PersonaBatch
from prompts.persona_generator_prompt import PERSONA_GENERATOR_PROMPT

PERSONAS_PATH = "data/personas.json"

def generate_personas(n: int = 20) -> list[Persona]:
    llm = get_chat_model("persona_generator", temperature=1.1)
    structured_llm = llm.with_structured_output(PersonaBatch)

    batch: PersonaBatch = structured_llm.invoke(
        PERSONA_GENERATOR_PROMPT.format(n=n)
    )
    return batch.personas

def save_personas(personas: list[Persona], path: str = PERSONAS_PATH, append: bool = True):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    existing_data = []
    if append and file_path.exists():
        existing_data = json.loads(file_path.read_text(encoding="utf-8"))

    existing_ids = {p["id"] for p in existing_data}
    new = [p.model_dump() for p in personas if p.id not in existing_ids]

    all = existing_data + new
    file_path.write_text(json.dumps(all, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(new)} new personas saved. Total: {len(all)}")


def load_personas(path: str = PERSONAS_PATH) -> list[Persona]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Persona(**p) for p in data]


def pick_random_persona(path: str = PERSONAS_PATH) -> Persona:
    personas = load_personas(path)
    if not personas:
        raise ValueError("No persona found. Run generate_personas() first.")
    return random.choice(personas)

if __name__ == "__main__":
    personas = generate_personas(20)
    save_personas(personas)