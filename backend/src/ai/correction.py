import json

import openai
from pydantic import ValidationError

from src.ai.client import get_openai_client
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.ai.prompts import CORRECTION_SYSTEM, CORRECTION_USER
from src.ai.schemas import CorrectionOutput
from src.config import settings

CORRECTION_RETRY_HINT = (
    "IMPORTANT: Your previous response did not match the required schema. "
    "Return ONLY a valid JSON object with: "
    "score (float between 0.0 and 1.0), "
    "mistakes (list of strings, empty list if all answers are correct)."
)


async def call_correction(
    questions: list[str], user_answers: list[str], hint: str | None = None
) -> CorrectionOutput:
    client = get_openai_client()
    pairs = "\n".join(
        f"Q{i + 1}: {q}\nA{i + 1}: {a}"
        for i, (q, a) in enumerate(zip(questions, user_answers))
    )
    user_content = CORRECTION_USER.format(pairs=pairs)
    if hint is not None:
        user_content = user_content + "\n\n" + hint
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CORRECTION_SYSTEM},
                {"role": "user", "content": user_content},
            ],
        )
    except (openai.APIError, openai.APITimeoutError, openai.RateLimitError) as exc:
        raise AITransientError(str(exc)) from exc

    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
        return CorrectionOutput.model_validate(parsed)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise AIOutputValidationError(str(exc)) from exc
