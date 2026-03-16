from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas import AnswerOptionCreate

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1)
    question_type: str = "single_choice"
    order_index: int = 0
    points: float = 1.0
    test_Id: Optional[int] = Field(default=None, description="айди теста в котором должен присутствовать этот вопрос")

class QuestionCreate(QuestionBase):
    options: list[AnswerOptionCreate] = []

class QuestionUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1)
    question_type: Optional[str] = None
    order_index: Optional[int] = None
    points: Optional[float] = None

class QuestionResponse(QuestionBase):
    Id: int
    test_id: int
    created_at: datetime
    updated_at: datetime
    options: list["AnswerOptionResponse"] = []

    model_config = ConfigDict(from_attributes=True)