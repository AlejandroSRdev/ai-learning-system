"""All DB access for the learning_state table."""


async def get_state(pool, student_id: int) -> dict:
    row = await pool.fetchrow(
        "SELECT * FROM learning_state WHERE student_id = $1 ORDER BY updated_at DESC LIMIT 1",
        student_id,
    )
    if row is None:
        raise ValueError(f"No learning state for student {student_id}")
    return dict(row)


async def update_state(pool, student_id: int, score: float, iteration: int) -> None:
    await pool.execute(
        "UPDATE learning_state SET last_score = $2, iteration = $3, updated_at = NOW() WHERE student_id = $1",
        student_id,
        score,
        iteration,
    )


async def create_state(pool, student_id: int, current_topic: str) -> None:
    await pool.execute(
        "INSERT INTO learning_state (student_id, current_topic, last_score, iteration) VALUES ($1, $2, NULL, 0)",
        student_id,
        current_topic,
    )
