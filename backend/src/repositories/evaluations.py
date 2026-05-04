import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_average_score(session: AsyncSession, student_id: int) -> float:
    result = await session.scalar(
        text("SELECT COALESCE(AVG(score), 0.0) FROM evaluations WHERE student_id = :student_id"),
        {"student_id": student_id},
    )
    return float(result)


async def save_evaluation(
    session: AsyncSession,
    student_id: int,
    topic: str,
    questions: dict,
    answers: dict,
    score: float,
) -> None:
    await session.execute(
        text(
            "INSERT INTO evaluations (student_id, topic, questions, answers, score)"
            " VALUES (:student_id, :topic, :questions, :answers, :score)"
        ),
        {
            "student_id": student_id,
            "topic": topic,
            "questions": json.dumps(questions),
            "answers": json.dumps(answers),
            "score": score,
        },
    )
