"""Orchestrates correction flow: grades answers, updates learning state, returns decision."""

from src.ai.correction import CORRECTION_RETRY_HINT, call_correction
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.domain.decisions import decide_next_step
from src.repositories import evaluations, learning_state


async def process_correction(
    student_id: int, questions: list[str], answers: list[str], pool
) -> dict:
    state = await learning_state.get_state(pool, student_id)
    try:
        result = await call_correction(questions=questions, user_answers=answers)
    except AITransientError:
        result = await call_correction(questions=questions, user_answers=answers)
    except AIOutputValidationError:
        result = await call_correction(
            questions=questions, user_answers=answers, hint=CORRECTION_RETRY_HINT
        )
    await evaluations.save_evaluation(
        pool,
        student_id,
        topic=state["current_topic"],
        questions={"items": questions},
        answers={"items": answers},
        score=result.score,
    )
    await learning_state.update_state(
        pool, student_id, score=result.score, iteration=state["iteration"] + 1
    )
    decision = decide_next_step(result.score)
    return {"score": result.score, "decision": decision}
