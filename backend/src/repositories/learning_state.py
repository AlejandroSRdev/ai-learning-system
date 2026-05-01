"""All DB access for the learning_state table."""


async def get_state(pool, student_id: int) -> dict:
    pass


async def update_state(pool, student_id: int, score: float, iteration: int) -> None:
    pass
