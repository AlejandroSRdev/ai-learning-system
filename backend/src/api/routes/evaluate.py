from fastapi import APIRouter

router = APIRouter()


@router.post("/{student_id}")
async def evaluate(student_id: int):
    return {"status": "not_implemented"}
