"""All DB access for the evaluations table."""


async def get_average_score(pool, student_id: int) -> float:
    result = await pool.fetchval(
        "SELECT COALESCE(AVG(score), 0.0) FROM evaluations WHERE student_id = $1",
        student_id,
    )
    return float(result)


async def save_evaluation(
    pool,
    student_id: int,
    topic: str,
    questions: dict,
    answers: dict,
    score: float,
) -> None:
    await pool.execute(
        "INSERT INTO evaluations (student_id, topic, questions, answers, score) VALUES ($1, $2, $3, $4, $5)",
        student_id,
        topic,
        questions,
        answers,
        score,
    )
