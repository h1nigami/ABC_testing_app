from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from .question import QuestionResponse, QuestionCreate

class TestBase(BaseModel):
    __test__ = False

    title: str = Field(..., min_length=1 ,max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    is_published: bool = False

class TestCreate(TestBase):
    pass

class TestWithQuestionCreate(TestCreate):
    questions: list[QuestionCreate] = []

class TestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1 ,max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    is_published: Optional[bool] = False    

class TestResponse(TestBase):
    Id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    questions: list[QuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)