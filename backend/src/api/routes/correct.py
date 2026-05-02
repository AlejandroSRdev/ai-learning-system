from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator, model_validator

from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.api.deps import get_pool
from src.services.correct import process_correction

router = APIRouter()


class CorrectRequest(BaseModel):
    questions: list[str]
    answers: list[str]

    @field_validator("questions")
    @classmethod
    def validate_questions(cls, v: list[str]) -> list[str]:
        if len(v) != 10:
            raise ValueError("questions must have exactly 10 items")
        for item in v:
            if not item.strip():
                raise ValueError("each question must be a non-empty string")
        return v

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v: list[str]) -> list[str]:
        if len(v) != 10:
            raise ValueError("answers must have exactly 10 items")
        for item in v:
            if not item.strip():
                raise ValueError("each answer must be a non-empty string")
        return v

    @model_validator(mode="after")
    def check_lengths_match(self) -> "CorrectRequest":
        if len(self.questions) != len(self.answers):
            raise ValueError("questions and answers must have the same length")
        return self


@router.post("/{student_id}")
async def correct(student_id: int, body: CorrectRequest, pool=Depends(get_pool)):
    try:
        return await process_correction(student_id, body.questions, body.answers, pool)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AIOutputValidationError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except AITransientError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
