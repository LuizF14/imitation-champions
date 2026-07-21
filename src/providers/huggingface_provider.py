import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification, BitsAndBytesConfig
from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
LORA_PATH = "./models/qwen-judge-classifier"

_model = None

class ClassifierModel:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def classify(self, text):
        id2label = {0: "HUMAN", 1: "AI"} 
        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.model.device)

            logits = self.model(**inputs).logits
            predicted_id = torch.argmax(logits, dim=-1).item()
            predicted_verdict = id2label[predicted_id]

            return predicted_verdict

def get_huggingface_model():
    global _model

    if _model is not None:
        return _model

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

    _model = ClassifierModel(model, tokenizer)
    return _model