import json

import openai
from pydantic import ValidationError

from src.ai.client import get_openai_client
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.ai.prompts import EXPLANATION_SYSTEM, EXPLANATION_USER
from src.ai.schemas import ExplanationOutput
from src.config import settings

EXPLANATION_RETRY_HINT = (
    "IMPORTANT: Your previous response did not match the required schema. "
    "Return ONLY a valid JSON object with exactly these fields: "
    "title (string), body (string), key_concepts (list of 3 to 6 strings), "
    "difficulty_applied (string)."
)


async def call_explanation(
    topic: str, level: str, difficulty: str, average_score: float, evaluation_note: str, hint: str | None = None
) -> ExplanationOutput:
    client = get_openai_client()
    user_content = EXPLANATION_USER.format(
        topic=topic, level=level, difficulty=difficulty,
        average_score=average_score, evaluation_note=evaluation_note
    )
    if hint is not None:
        user_content = user_content + "\n\n" + hint
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.6,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": EXPLANATION_SYSTEM},
                {"role": "user", "content": user_content},
            ],
        )
    except (openai.APIError, openai.APITimeoutError, openai.RateLimitError) as exc:
        raise AITransientError(str(exc)) from exc

    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
        return ExplanationOutput.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise AIOutputValidationError(str(exc)) from exc
