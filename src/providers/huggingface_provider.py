import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline


BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
LORA_PATH = "./models/qwen-turing-judge"

_model = None

def get_huggingface_model(temperature: float = 0.7):
    global _model

    if _model is not None:
        return _model

    tokenizer = AutoTokenizer.from_pretrained(LORA_PATH)

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        dtype=torch.float16,
        device_map="auto",
    )

    hf_model = PeftModel.from_pretrained(base_model, LORA_PATH)
    hf_model.eval() 

    pipe = pipeline(
        "text-generation",
        model=hf_model,      
        tokenizer=tokenizer,
        max_new_tokens=256,
        max_length=None,
        do_sample=True,
        temperature=temperature,
        return_full_text=False,
    )

    llm = HuggingFacePipeline(pipeline=pipe)
    _model = ChatHuggingFace(llm=llm)

    return _model