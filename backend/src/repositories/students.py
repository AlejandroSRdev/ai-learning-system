from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_student(session: AsyncSession, student_id: int) -> dict:
    result = await session.execute(
        text("SELECT id, level, goal, created_at FROM students WHERE id = :student_id"),
        {"student_id": student_id},
    )
    row = result.mappings().one_or_none()
    if row is None:
        raise ValueError(f"Student {student_id} not found")
    return dict(row)


async def create_student(session: AsyncSession, level: str, goal: str) -> dict:
    result = await session.execute(
        text("INSERT INTO students (level, goal) VALUES (:level, :goal) RETURNING *"),
        {"level": level, "goal": goal},
    )
    row = result.mappings().one()
    return dict(row)
