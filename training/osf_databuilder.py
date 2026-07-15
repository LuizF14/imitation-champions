import pandas as pd

from datasets import Dataset

from sklearn.model_selection import train_test_split


SYSTEM_PROMPT = """
You are an expert judge in the Turing Test.

You will receive a conversation between an interrogator (I)
and a witness (W).

Your task is to determine whether the witness is a HUMAN or an AI.

Answer using only one of the following words:

HUMAN
AI
""".strip()


def create_sample(prefix: str, is_human: bool):
    answer = "HUMAN" if is_human else "AI"

    return {
        "messages": [
            { "role": "system","content": SYSTEM_PROMPT },
            { "role": "user","content": prefix },
            { "role": "assistant","content": answer },
        ]
    }


def build_dataset():
    df = pd.read_csv("training/datasets/osf-3party/data/tt_transcripts.csv")
    conversations = []

    for _, row in df.iterrows():
        transcript = row["transcript"]
        is_human = row["is_human"]

        turns = transcript.split("\n")
        samples = []

        for i in range(4, len(turns) + 1, 2):
            prefix = "\n".join(turns[:i])
            samples.append(create_sample(prefix, is_human))
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