from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_student(body: dict):
    return {"status": "not_implemented"}


@router.get("/{student_id}/state")
async def get_student_state(student_id: int):
    return {"status": "not_implemented"}
