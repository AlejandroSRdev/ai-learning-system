from pydantic import BaseModel, field_validator, model_validator


class Question(BaseModel):
    question: str
    options: list[str]
    correct_answer: str

    @field_validator("options")
    @classmethod
    def check_options_count(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("options must have exactly 4 items")
        return v

    @model_validator(mode="after")
    def check_correct_answer_in_options(self) -> "Question":
        if self.correct_answer not in self.options:
            raise ValueError("correct_answer must be one of the provided options")
        return self


class ExplanationOutput(BaseModel):
    title: str
    body: str
    key_concepts: list[str]
    difficulty_applied: str

    @field_validator("key_concepts")
    @classmethod
    def check_key_concepts_count(cls, v: list[str]) -> list[str]:
        if not (3 <= len(v) <= 6):
            raise ValueError("key_concepts must have between 3 and 6 items")
        return v


class EvaluationOutput(BaseModel):
    questions: list[Question]

    @model_validator(mode="after")
    def check_question_count(self) -> "EvaluationOutput":
        if len(self.questions) != 10:
            raise ValueError(f"Expected 10 questions, got {len(self.questions)}")
        return self


class CorrectionOutput(BaseModel):
    score: float
    mistakes: list[str]

    @field_validator("score")
    @classmethod
    def check_score_range(cls, v: float) -> float:
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Score must be between 0.0 and 1.0, got {v}")
        return v
