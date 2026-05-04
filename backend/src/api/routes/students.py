from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_db
from src.repositories import learning_state, students

router = APIRouter()


class CreateStudentRequest(BaseModel):
    level: str
    goal: str
    current_topic: str

    @field_validator("level", "goal", "current_topic", mode="before")
    @classmethod
    def normalize_and_validate(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("must not be empty")
        if len(v) > 200:
            raise ValueError("must not exceed 200 characters")
        return v


@router.post("")
async def create_student(body: CreateStudentRequest, session: AsyncSession = Depends(get_db)):
    student = await students.create_student(session, body.level, body.goal)
    await learning_state.create_state(session, student["id"], body.current_topic)
    await session.commit()
    return {"student_id": student["id"]}


@router.get("/{student_id}/state")
async def get_student_state(student_id: int):
    return {"status": "not_implemented"}
