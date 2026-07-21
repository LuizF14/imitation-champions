import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

from judge_classifier_dataset import build_dataset

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
LORA_PATH = "./models/qwen-judge-classifier"

tokenizer = AutoTokenizer.from_pretrained(LORA_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

base_model = AutoModelForSequenceClassification.from_pretrained(
    BASE_MODEL,
    num_labels=2,
    quantization_config=bnb_config,
    device_map="auto",
)
base_model.config.pad_token_id = tokenizer.pad_token_id

model = PeftModel.from_pretrained(base_model, LORA_PATH)
model.eval()

train_dataset, test_dataset, val_dataset = build_dataset()

id2label = {0: "HUMAN", 1: "AI"} 

correct = 0
results = []

with torch.no_grad():
    for sample in tqdm(test_dataset, desc="Avaliando previsões", unit="amostra"):
        inputs = tokenizer(
            sample["text"],
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(model.device)

        logits = model(**inputs).logits
        predicted_id = torch.argmax(logits, dim=-1).item()
        predicted_verdict = id2label[predicted_id]

        expected_id = sample["label"]
        expected_verdict = id2label[expected_id]

        is_correct = predicted_verdict == expected_verdict
        if is_correct:
            correct += 1

        results.append({
            "expected_verdict": expected_verdict,
            "predicted_verdict": predicted_verdict,
            "is_correct": is_correct,
            "text": sample["text"],
        })

df_results = pd.DataFrame(results)

accuracy = correct / len(test_dataset)
print(f"\nAccuracy: {accuracy:.3%}")

df_results.to_csv("results/judge_evaluation_qwen2_5_classifier.csv", index=False)
print("Resultados salvos com sucesso em 'results/judge_evaluation_qwen2_5_classifier.csv'!")