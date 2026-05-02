"""Orchestrates explanation flow: fetches student state, determines difficulty, calls AI layer."""

from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.ai.explanation import EXPLANATION_RETRY_HINT, call_explanation
from src.repositories import learning_state, students


async def generate_explanation(student_id: int, pool) -> dict:
    student = await students.get_student(pool, student_id)
    state = await learning_state.get_state(pool, student_id)

    average_score = state["average_score"]
    if average_score < 0.5:
        difficulty = "basic"
    elif average_score < 0.75:
        difficulty = "intermediate"
    else:
        difficulty = "advanced"

    try:
        result = await call_explanation(
            topic=state["current_topic"],
            level=student["level"],
            difficulty=difficulty,
            average_score=average_score,
            evaluation_note=state["last_evaluation_note"],
        )
    except AITransientError:
        result = await call_explanation(
            topic=state["current_topic"],
            level=student["level"],
            difficulty=difficulty,
            average_score=average_score,
            evaluation_note=state["last_evaluation_note"],
        )
    except AIOutputValidationError:
        result = await call_explanation(
            topic=state["current_topic"],
            level=student["level"],
            difficulty=difficulty,
            average_score=average_score,
            evaluation_note=state["last_evaluation_note"],
            hint=EXPLANATION_RETRY_HINT,
        )

    return result.model_dump()
