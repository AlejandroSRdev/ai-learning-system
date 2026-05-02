"""Orchestrates evaluation flow: fetches current topic, calls AI layer to generate questions."""

from src.ai.evaluation import EVALUATION_RETRY_HINT, call_evaluation
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.repositories import learning_state, students


async def generate_evaluation(student_id: int, pool) -> dict:
    student = await students.get_student(pool, student_id)
    state = await learning_state.get_state(pool, student_id)
    try:
        result = await call_evaluation(topic=state["current_topic"], level=student["level"])
    except AITransientError:
        result = await call_evaluation(topic=state["current_topic"], level=student["level"])
    except AIOutputValidationError:
        result = await call_evaluation(
            topic=state["current_topic"],
            level=student["level"],
            hint=EVALUATION_RETRY_HINT,
        )
    return result.model_dump()
