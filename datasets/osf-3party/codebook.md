## AI Models Table (`tt_aimodel.csv`)

This table contains information about the AI systems that participated in the Turing test experiment as witnesses.

| Variable | Description |
|----------|-------------|
| id | Unique identifier for the AI model |
| name | Name identifier for the model (e.g., "gpt-4o_minimal_sona") |
| family | Classification of the model type (e.g., "control", "no-persona", "llama-persona") |
| model_name | The technical model identifier (e.g., "gpt-4.5-preview-2025-02-27") |
| active | Boolean indicating if the model was active during the study |
| prompt_id | Foreign key referencing the prompt template used with this model |
| prompt_extra | Any additional text appended to the model's main prompt |
| temperature | The sampling temperature used for model generations (higher = more random) |
| secs_per_char | The artificial delay in seconds per character used when displaying model responses |
| max_length | Maximum allowed length of model responses |
| response_method | Technical method used to generate responses (e.g., "openai_response", "eliza_response") |
| wins | Number of games where interrogators incorrectly identified this model as human |
| losses | Number of games where interrogators correctly identified this model as AI |
| weighted_wins | Weighted score of wins (accounting for confidence) |
| weighted_losses | Weighted score of losses (accounting for confidence) |
| batch | Study batch identifier |
| city | Location context provided in the model's prompt |

### Notes
- Models fell into several categories: GPT-4.5 (with/without persona), LLaMa-3.1-405B (with/without persona), GPT-4o, and ELIZA
- The "PERSONA" prompt variants instructed the model to adopt a young, introverted persona knowledgeable about internet culture
- The "NO-PERSONA" prompt variants provided minimal instructions with contextual information