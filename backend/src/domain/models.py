from dataclasses import dataclass
from datetime import datetime


@dataclass
class Student:
    id: int
    level: str
    goal: str
    created_at: datetime


@dataclass
class LearningState:
    id: int
    student_id: int
    current_topic: str
    last_score: float
    iteration: int
    updated_at: datetime
    average_score: float = 0.0
    last_evaluation_note: str = ""


@dataclass
class Evaluation:
    id: int
    student_id: int
    topic: str
    questions: dict
    answers: dict
    score: float
    created_at: datetime
