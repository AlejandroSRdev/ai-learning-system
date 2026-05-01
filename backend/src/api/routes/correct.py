from fastapi import APIRouter

router = APIRouter()


@router.post("/{student_id}")
async def correct(student_id: int, body: dict):
    return {"status": "not_implemented"}
