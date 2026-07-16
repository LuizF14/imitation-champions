import pandas as pd

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from tqdm import tqdm

llm = ChatOllama(
    model="llama3.1",
    temperature=0.8,
)

human_sys_prompt = """
You are rewriting annotations from a Turing Test dataset.

Each annotation compares two conversations: one with a human and one with an AI.
The judge selected which participant was the human.

Your task is to rewrite the original justification so that it refers ONLY to the participant judged as HUMAN.

If the original justification only criticizes the AI, rewrite the complementary implication for the human using the smallest inference necessary.
Do not introduce new evidence or new personality traits.

Requirements:

- Write exactly one rewritten justification.
- Preserve the original meaning.
- Do NOT explain your reasoning.
- Do NOT mention the original justification.
- Do NOT mention the AI participant.
- Do NOT compare the participants.
- Keep it concise (one sentence).

Examples

Example 1
Human: B
AI: A

Original:
"really quick short answers did not take too much time to respond"

Rewritten:
"The participant responded quickly with concise answers."

Example 2
Human: A
AI: B

Original:
"too formal"

Rewritten:
"The participant's conversational style felt natural."

Example 3
Human: A
AI: B

Original:
"Too fast for B"

Rewritten:
"The participant responded at a natural conversational pace."

Example 4
Human: B
AI: A

Original:
"I don't think AI would say uhhh"

Rewritten:
"The participant used natural speech disfluencies."
"""

ai_sys_prompt = """
You are rewriting annotations from a Turing Test dataset.

Each annotation compares two conversations: one with a human and one with an AI.
The judge selected which participant was the human.

Your task is to rewrite the original justification so that it refers ONLY to the participant judged as AI.

If the original justification only praises the human, infer the corresponding weakness of the AI without inventing new evidence.
Do not introduce new evidence or new personality traits.

Requirements:

- Write exactly one rewritten justification.
- Preserve the original meaning.
- Do NOT explain your reasoning.
- Do NOT mention the original justification.
- Do NOT mention the AI participant.
- Do NOT compare the participants.
- Keep it concise (one sentence).

Examples

Example 1
Human: A
AI: B

Original:
"Witness B talked in a manner that was too nice whereas Witness A answered more chill."

Rewritten:
"The participant's responses felt overly polite and lacked a natural conversational tone."

Example 2
Human: A
AI: B

Original:
"They talked about finals, and made abrupt conversation like a person my age would."

Rewritten:
"The participant's conversation lacked the natural flow expected from a human."

Example 3
Human: B
AI: A

Original:
"They spoke more naturally and with slang (r, u, gl, etc.)"

Rewritten:
"The participant's responses lacked the natural use of informal language."

Example 4
Human: A
AI: B

Original:
"Witness B said my midterm at UCSD which is so vague and no one would ever say that"

Rewritten:
"The participant made vague statements that did not sound like something a person would naturally say."

Example 5
Human: B
AI: A

Original:
"I was almost fooled but witness B talked more informally, again."

Rewritten:
"The participant's responses sounded less natural and less informal than expected."
"""

human_prompt = ChatPromptTemplate.from_messages([("system", human_sys_prompt), ("human","Human participant: {participant}\n Original justification: {reason}")])
ai_prompt = ChatPromptTemplate.from_messages([("system", ai_sys_prompt), ("human","AI participant: {participant}\n Original justification: {reason}")])

human_chain = human_prompt | llm
ai_chain = ai_prompt | llm

df = pd.read_csv("datasets/osf-3party/data/tt_verdict.csv")

records = []

for i, row in tqdm(df.iterrows(), total=len(df), desc="Processando vereditos"):
    try:
        human = row["verdict"]
        ai = "B" if human == "A" else "A"

        human_reason = human_chain.invoke({
            "participant": human,
            "reason": row["reason"]
        }).content.strip()

        ai_reason = ai_chain.invoke({
            "participant": ai,
            "reason": row["reason"]
        }).content.strip()

        if human == "A":
            reason_a = human_reason
            reason_b = ai_reason
        else:
            reason_a = ai_reason
            reason_b = human_reason

        records.append(
            {
                "id": row["id"],
                "game_id": row["game_id"],
                "interrogator_id": row["interrogator_id"],
                "participant": "A",
                "label": "Human" if human == "A" else "AI",
                "reason": reason_a
            }
        )

        records.append(
            {
                "id": row["id"],
                "game_id": row["game_id"],
                "interrogator_id": row["interrogator_id"],
                "participant": "B",
                "label": "Human" if human == "B" else "AI",
                "reason": reason_b
            }
        )

    except Exception as e:
        # Usamos tqdm.write() para não quebrar a animação da barra de progresso no terminal
        tqdm.write(f"\nErro na linha {i}")
        tqdm.write(f"Reason original: {row['reason']}")
        tqdm.write(f"Erro: {e}")
        tqdm.write("-" * 80)

new_df = pd.DataFrame(records)
new_df.to_csv("datasets/osf-2party-synthetic/tt_verdict_individual.csv", index=False)
print("\nProcessamento concluído!")