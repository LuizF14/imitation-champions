<div align="center">

# 🤖 ImitationChampions

**A framework for building AI agents that talk like humans — and pass the Turing Test.**

[![Python](https://img.shields.io/badge/Python-3.11%2F3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-1C3C3C?style=flat)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=flat)](https://www.langchain.com/langgraph)
[![Multi-Provider](https://img.shields.io/badge/LLMs-Groq%20%7C%20Ollama%20%7C%20HuggingFace-F55036?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

</div>

---

## 🧠 What is this?

**ImitationChampions** is a framework for developing, testing, and benchmarking AI agents designed to be indistinguishable from humans in conversation — i.e., to pass the **Turing Test**.

It's built around a core conversational agent (powered by prompt engineering on top of LangChain), a suite of tools to generate realistic personas, an automatic AI judge to evaluate how convincingly human the bot sounds, and multiple interfaces to interact with it.

This project is a companion to **[ImitationGame](https://github.com/LuizF14/imitation-game)** (still in development), another project of mine — ImitationChampions exposes a REST API specifically so ImitationGame can talk to it directly.

---

## ✨ Key Features

- 🗣️ **Human-Like Conversational Agent** — built with prompt engineering on top of LangChain to sound natural and human
- 🎭 **Automatic Persona Generation** — uses AI to generate believable, consistent human personas
- ⚖️ **Automated AI Judge** — combines a fine-tuned classifier with an LLM-generated reasoning step to evaluate how convincingly human the bot sounds
- 🔌 **Configurable Providers & Models** — swap between **Groq, Ollama, and Hugging Face** with minimal config changes, running **Llama, Qwen, GPT, or Claude** models interchangeably
- 🌐 **Multiple Interfaces**:
  - Console app
  - **Streamlit** web frontend
  - **REST API** (used to integrate directly with the ImitationGame project)

---

## ⚖️ The Judge: A Fine-Tuned Classifier + LLM Reasoning

Instead of relying purely on prompting a general-purpose LLM to detect AI-generated text, ImitationChampions fine-tunes **Qwen2.5-3B with LoRA adapters** directly on real human-subject data — the **OSF 3-party Turing Test dataset** — producing `qwen-judge-classifier`: a lightweight sequence classifier (human vs. AI) built on top of `AutoModelForSequenceClassification`.

The classifier alone reached **80.06% accuracy** on the OSF 3-party Turing Test dataset.

The judge agent then combines the classifier's verdict with a second LLM call that generates a natural-language **reason** for the classification — so every verdict comes with both a label and an explanation of why the conversation read as human or AI.

Using a dataset from actual Turing Test experiments (rather than purely synthetic data) means the judge learns from how real interrogators, witnesses, and AI participants actually behaved — not just plausible-looking conversations.

The `notebooks/judges_comparison.ipynb` and `results/` directory contain a **head-to-head evaluation** of the vanilla Qwen2.5 model against the fine-tuned classifier, quantifying the accuracy gain from domain-specific fine-tuning.

---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangChain, LangGraph |
| Inference | Groq (fast serving), Hugging Face, Ollama (local) |
| Judge model | Qwen2.5-3B sequence classifier + LoRA (PEFT) fine-tuning |
| Interfaces | Streamlit, FastAPI-style REST API, CLI console |

---

## 📁 Project Structure

```
imitation-champions/
├── datasets/               # Turing Test training and evaluation dataset
├── models/
│   └── qwen-judge-classifier/  # Fine-tuned LoRA adapter for the judge classifier
├── notebooks/              # Judge comparison & evaluation notebooks
├── resources/              # Persona and judgement reference data
├── results/                # Judge evaluation results (base vs. fine-tuned)
├── scripts/                # Data rewriting / preprocessing utilities
├── src/
│   ├── agents/             # Conversational, interrogator, judge & persona agents
│   ├── interfaces/         # Console, Streamlit, and REST API frontends
│   ├── prompts/            # Prompt templates for each agent role
│   ├── providers/          # Groq / Hugging Face / Ollama LLM providers
│   ├── schemas/             # Pydantic schemas (conversation, persona, verdict)
│   ├── services/           # Business logic layer (conversation, judgement, persona)
│   └── tools/              # Utility tools (e.g. datetime tools for agents)
└── training/
    └── judge_classifier/    # Classifier training experiments
```

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/LuizF14/imitation-champions.git
cd imitation-champions

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

pip install -r requirements.txt

# Configure your provider API keys
cp .env.example .env
```

### Usage

Everything runs through a single CLI entry point:

```bash
python src/main.py <command> [options]
```

| Command | Description |
|---|---|
| `generate` | Generate new synthetic personas using AI |
| `console-chat` | Start a conversation with the bot in the terminal |
| `streamlit-chat` | Launch the Streamlit web frontend |
| `test-ai` | Run the AI judge against the bot in an automated benchmark |

**Generate personas**

```bash
python src/main.py generate -n 5 -o resources/personas.json
```

- `-n, --quantity` — number of personas to generate (default: `3`)
- `-o, --output` — output file path (default: `resources/personas.json`)
- `--no-append` — overwrite the output file instead of appending to it

**Chat with the bot (console)**

```bash
python src/main.py console-chat
```

**Chat with the bot (Streamlit web UI)**

```bash
python src/main.py streamlit-chat
```

**Benchmark the bot with the AI judge**

```bash
python src/main.py test-ai -c 10 -t 6
```

- `-c, --conversations` — number of conversations to evaluate (default: `10`)
- `-t, --turns` — number of turns per conversation (default: `6`)

Runs an automated benchmark where the judge evaluates how convincingly human the bot sounds, and writes the results to `resources/judgement.json`.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built by [Luiz Felipe](https://github.com/LuizF14) — Computer Engineering @ UNIFEI

</div>
