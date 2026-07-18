import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split

from judge_sys_prompt import SYSTEM_PROMPT

def create_sample(prefix: str, is_human: bool):
    text = f"""

{SYSTEM_PROMPT}

Conversation:
{prefix}
"""

    return {
        "text": text,
        "label": int(is_human),
    }

def build_dataset():
    transcripts_df = pd.read_csv("datasets/osf-3party/data/tt_transcripts.csv")
    conversations = []

    for _, row in transcripts_df.iterrows():
        transcript = row["transcript"]
        is_human = row["is_human"]

        turns = transcript.split("\n")
        samples = []

        for i in range(4, len(turns) + 1, 2):
            prefix = "\n".join(turns[:i])
            samples.append(create_sample(prefix, is_human))
        conversations.append(samples)

    labels = transcripts_df["is_human"].tolist()

    train_conversations, temp_conversations, train_labels, temp_labels = train_test_split(
        conversations,
        labels,
        test_size=0.2,
        stratify=labels,
        random_state=42,
    )

    val_conversations, test_conversations, val_labels, test_labels = train_test_split(
        temp_conversations,
        temp_labels,
        test_size=0.5,
        stratify=temp_labels,
        random_state=42,
    )

    train = [ sample for conversation in train_conversations for sample in conversation ]
    test = [ sample for conversation in test_conversations for sample in conversation ]
    val = [ sample for conversation in val_conversations for sample in conversation ]

    return (
        Dataset.from_list(train),
        Dataset.from_list(test),
        Dataset.from_list(val)
    )