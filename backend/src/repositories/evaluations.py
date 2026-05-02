"""All DB access for the evaluations table."""


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
