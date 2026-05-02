"""All DB access for the students table."""


async def get_student(pool, student_id: int) -> dict:
    row = await pool.fetchrow(
        "SELECT id, level, goal, created_at FROM students WHERE id = $1",
        student_id,
    )
    if row is None:
        raise ValueError(f"Student {student_id} not found")
    return dict(row)


async def create_student(pool, level: str, goal: str) -> dict:
    row = await pool.fetchrow(
        "INSERT INTO students (level, goal) VALUES ($1, $2) RETURNING *",
        level,
        goal,
    )
    return dict(row)
