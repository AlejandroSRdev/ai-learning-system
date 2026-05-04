from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_state(session: AsyncSession, student_id: int) -> dict:
    result = await session.execute(
        text(
            "SELECT id, student_id, current_topic, last_score, iteration, average_score,"
            " last_evaluation_note, updated_at"
            " FROM learning_state WHERE student_id = :student_id ORDER BY updated_at DESC LIMIT 1"
        ),
        {"student_id": student_id},
    )
    row = result.mappings().one_or_none()
    if row is None:
        raise ValueError(f"No learning state for student {student_id}")
    return dict(row)


async def update_state(
    session: AsyncSession,
    student_id: int,
    score: float,
    iteration: int,
    average_score: float,
    evaluation_note: str,
) -> None:
    await session.execute(
        text(
            "UPDATE learning_state"
            " SET last_score = :score, iteration = :iteration, average_score = :average_score,"
            " last_evaluation_note = :evaluation_note, updated_at = NOW()"
            " WHERE student_id = :student_id"
        ),
        {
            "student_id": student_id,
            "score": score,
            "iteration": iteration,
            "average_score": average_score,
            "evaluation_note": evaluation_note,
        },
    )


async def create_state(session: AsyncSession, student_id: int, current_topic: str) -> None:
    await session.execute(
        text(
            "INSERT INTO learning_state (student_id, current_topic, last_score, iteration)"
            " VALUES (:student_id, :current_topic, NULL, 0)"
        ),
        {"student_id": student_id, "current_topic": current_topic},
    )
