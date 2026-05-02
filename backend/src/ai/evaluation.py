import json

import openai
from pydantic import ValidationError

from src.ai.client import get_openai_client
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.ai.prompts import EVALUATION_SYSTEM, EVALUATION_USER
from src.ai.schemas import EvaluationOutput
from src.config import settings

EVALUATION_RETRY_HINT = (
    "IMPORTANT: Your previous response did not match the required schema. "
    "Return EXACTLY 10 question objects. Each must have: "
    "question (string), options (list of exactly 4 strings), "
    "correct_answer (one string that matches one of the options exactly)."
)


async def call_evaluation(
    topic: str, level: str, hint: str | None = None
) -> EvaluationOutput:
    client = get_openai_client()
    user_content = EVALUATION_USER.format(topic=topic, level=level)
    if hint is not None:
        user_content = user_content + "\n\n" + hint
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.3,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": EVALUATION_SYSTEM},
                {"role": "user", "content": user_content},
            ],
        )
    except (openai.APIError, openai.APITimeoutError, openai.RateLimitError) as exc:
        raise AITransientError(str(exc)) from exc

    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
        return EvaluationOutput.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise AIOutputValidationError(str(exc)) from exc
