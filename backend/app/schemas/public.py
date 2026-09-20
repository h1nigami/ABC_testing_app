from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AnswerOptionPublic(BaseModel):
    """Вариант ответа без пометки о правильности (для прохождения теста учеником)."""
    Id: int
    question_id: int
    text: str
    order_index: int

    model_config = ConfigDict(from_attributes=True)


class QuestionPublic(BaseModel):
    Id: int
    text: str
    question_type: str
    order_index: int
    points: float
    options: list[AnswerOptionPublic] = []

    model_config = ConfigDict(from_attributes=True)


class TestPublic(BaseModel):
    __test__ = False

    Id: int
    title: str
    description: Optional[str] = None
    is_published: bool
    questions: list[QuestionPublic] = []

    model_config = ConfigDict(from_attributes=True)
