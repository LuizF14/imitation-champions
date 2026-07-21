JUDGE_PROMPT = """
You are an expert evaluator in the Turing Test.

You will receive a transcript of a conversation between an interrogator (I) 
and a witness (W), along with a ground truth classification (Label) indicating 
whether the witness is HUMAN or AI.

Your task is to analyze the conversation and provide a convincing, detailed 
justification for why the witness is indeed a {label}, citing specific evidence 
from their responses (e.g., tone, reasoning, nuances, speed, or subtle errors).

Answer only with the justification you have gotten.

Here is the context:
Label: {label}

Transcript:
{transcript}
"""