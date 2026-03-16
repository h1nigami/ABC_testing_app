from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AnswerOptionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=255)
    is_correct: bool = Field(..., description="Is this answer correct?")
    order_index: int = Field(..., description="Order index of the answer option")

class AnswerOptionCreate(AnswerOptionBase):
    pass    

class AnswerOptionUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=255)
    is_correct: Optional[bool] = Field(None, description="Is this answer correct?")
    order_index: Optional[int] = Field(None, description="Order index of the answer option")

class AnswerOptionResponse(AnswerOptionBase):
    Id: int
    question_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )