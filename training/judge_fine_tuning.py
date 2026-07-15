import torch

from transformers import (AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig,TrainingArguments)
from peft import (LoraConfig,prepare_model_for_kbit_training,get_peft_model,)
from trl.trainer.sft_trainer import SFTTrainer 
from trl.trainer.sft_config import SFTConfig
from osf_databuilder import build_dataset

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="cuda",
    dtype=torch.float32,
)

model = prepare_model_for_kbit_training(model)

model.config.use_cache = False
model.gradient_checkpointing_enable()

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
    bias="none",
    task_type="CAUSAL_LM",
    inference_mode=False,
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
print(f"Modelo carregado!\nDevice: {model.device}\nVRAM: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

for name, param in model.named_parameters():
    if param.requires_grad:
        print("ANTES DO SFTTrainer:", name, param.dtype)
        break

train_dataset, eval_dataset = build_dataset()

training_args = SFTConfig(
    output_dir="./models/qwen-turing-judge",
    num_train_epochs=3,
    learning_rate=2e-4,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    fp16=True,
    bf16=False,
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    warmup_steps=50,         
    weight_decay=0.01,
    logging_steps=10,
    logging_first_step=True,
    save_strategy="steps",
    save_steps=100,
    eval_strategy="steps",
    eval_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    report_to="none",
    seed=42,
    max_length=512,
    packing=False,
    assistant_only_loss=True,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
)

for param in model.parameters():
    if param.requires_grad:
        param.data = param.data.to(torch.float32)

trainer.train()

trainer.save_model("./models/qwen-turing-judge")
tokenizer.save_pretrained("./models/qwen-turing-judge")