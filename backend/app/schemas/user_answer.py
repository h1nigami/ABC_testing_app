from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserAnswerBase(BaseModel):
    attempt_id: int
    question_id: int 
    selected_option_id: int

class UserAnswerCreate(UserAnswerBase):
    pass

class UserAnswerResponse(UserAnswerBase):
    Id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 