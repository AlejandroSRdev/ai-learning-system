from pydantic import BaseModel


class ExplanationOutput(BaseModel):
    content: str


class EvaluationOutput(BaseModel):
    questions: list[dict]


class CorrectionOutput(BaseModel):
    score: float
    mistakes: list[str]
