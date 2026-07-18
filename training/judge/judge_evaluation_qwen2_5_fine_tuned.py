import torch
import pandas as pd

from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from osf_databuilder import build_dataset
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
LORA_PATH = "./models/qwen-turing-judge"

tokenizer = AutoTokenizer.from_pretrained(LORA_PATH)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float16,
    device_map="auto",
)

model = PeftModel.from_pretrained(model, LORA_PATH)
model.eval()

_, test_dataset, _ = build_dataset()


def generate(messages):
    prompt = tokenizer.apply_chat_template(
        messages[:-1],
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=False,
            temperature=0.0,
        )

    return tokenizer.decode(
        output[0][inputs.input_ids.shape[1]:],
        skip_special_tokens=True,
    )

def parse_response(text: str):
    verdict = None
    reason_lines = []
    reading_reason = False

    for line in text.splitlines():
        line = line.strip()

        if line.lower().startswith("verdict:"):
            verdict = line.split(":", 1)[1].strip()
            reading_reason = False

        elif line.lower().startswith("reason:"):
            reason_lines.append(line.split(":", 1)[1].strip())
            reading_reason = True

        elif reading_reason:
            reason_lines.append(line)

    reason = "\n".join(reason_lines).strip()

    return verdict, reason

correct = 0
results = []

for sample in tqdm(test_dataset, desc="Avaliando previsões", unit="amostra"):
    prediction = generate(sample["messages"])
    expected = sample["messages"][-1]["content"]

    expected_verdict, expected_reason = parse_response(expected)
    predicted_verdict, predicted_reason = parse_response(prediction)

    is_correct = False
    if expected_verdict is not None and predicted_verdict is not None and expected_verdict.upper() == predicted_verdict.upper():
        correct += 1
        is_correct = True

    results.append({
        "num_conversation_messages": len(sample["messages"]) - 1,              # Conta apenas a conversa de Turing (sem o veredito)
        "expected_verdict": expected_verdict,
        "predicted_verdict": predicted_verdict,
        "is_correct": is_correct,
        "expected_reason": expected_reason,
        "predicted_reason": predicted_reason,
        "messages_history": str(sample["messages"][:-1]) 
    })

df_results = pd.DataFrame(results)

accuracy = correct / len(test_dataset)
print(f"\nAccuracy: {accuracy:.3%}")

df_results.to_csv("results/judge_evaluation_qwen2_5_fine_tuned.csv", index=False)
print("Resultados salvos com sucesso em 'results/judge_evaluation_qwen2_5_fine_tuned.csv'!")