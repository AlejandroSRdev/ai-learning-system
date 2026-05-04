"""Orchestrates correction flow: grades answers, updates learning state, returns decision."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.correction import CORRECTION_RETRY_HINT, call_correction
from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.domain.decisions import decide_next_step
from src.repositories import evaluations, learning_state


async def process_correction(
    student_id: int, questions: list[str], answers: list[str], session: AsyncSession
) -> dict:
    state = await learning_state.get_state(session, student_id)
    try:
        result = await call_correction(questions=questions, user_answers=answers)
    except AITransientError:
        result = await call_correction(questions=questions, user_answers=answers)
    except AIOutputValidationError:
        result = await call_correction(
            questions=questions, user_answers=answers, hint=CORRECTION_RETRY_HINT
        )
    await evaluations.save_evaluation(
        session,
        student_id,
        topic=state["current_topic"],
        questions={"items": questions},
        answers={"items": answers},
        score=result.score,
    )
    average_score = await evaluations.get_average_score(session, student_id)
    evaluation_note = result.evaluation_note
    await learning_state.update_state(
        session,
        student_id,
        score=result.score,
        iteration=state["iteration"] + 1,
        average_score=average_score,
        evaluation_note=evaluation_note,
    )
    await session.commit()
    decision = decide_next_step(result.score)
    return {"score": result.score, "decision": decision}
