import pandas as pd

from datasets import Dataset

from sklearn.model_selection import train_test_split


SYSTEM_PROMPT = """
You are an expert judge in the Turing Test.

You will receive a conversation between an interrogator (I)
and a witness (W).

Your task is to determine whether the witness is HUMAN or AI
and briefly justify your decision.

Answer using exactly this format:

Verdict: HUMAN
Reason: ...

or

Verdict: AI
Reason: ...
""".strip()


def create_sample(prefix: str, is_human: bool, reason: str):
    answer = "HUMAN" if is_human else "AI"

    return {
        "messages": [
            { "role": "system","content": SYSTEM_PROMPT },
            { "role": "user","content": prefix },
            { "role": "assistant", "content": f"Verdict: {answer}\nReason: {reason}" },
        ]
    }


def build_dataset():
    transcripts_df = pd.read_csv("datasets/osf-3party/data/tt_transcripts.csv")
    verdicts_df = pd.read_csv("datasets/osf-2party-synthetic/tt_verdict_individual.csv")
    conversations = []

    transcripts_df = transcripts_df.drop(columns=["reason"])
    transcripts_df["label"] = transcripts_df["is_human"].map({
        True: "Human",
        False: "AI",
    })

    df = transcripts_df.merge(
        verdicts_df[["game_id", "label", "reason"]],
        on=["game_id", "label"],
        how="left",
    )

    for _, row in df.iterrows():
        transcript = row["transcript"]
        is_human = row["is_human"]
        reason = row["reason"]

        turns = transcript.split("\n")
        samples = []

        for i in range(4, len(turns) + 1, 2):
            prefix = "\n".join(turns[:i])
            samples.append(create_sample(prefix, is_human, reason))
        conversations.append(samples)

    labels = df["is_human"].tolist()

    train, test = train_test_split(
        conversations,
        test_size=0.2,
        stratify=labels,
        random_state=42,
    )

    train = [ sample for conversation in train for sample in conversation ]

    test = [ sample for conversation in test for sample in conversation ]

    return (
        Dataset.from_list(train),
        Dataset.from_list(test),
    )