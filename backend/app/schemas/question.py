from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1)
    question_type: str = "single_choice"
    order_index: int = 0
    points: float = 1.0

class QuestionCreate(QuestionBase):
    test_id: int
    options: list["AnswerOptionCreate"] = []

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