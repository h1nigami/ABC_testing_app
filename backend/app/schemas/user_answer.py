from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class UserAnswerBase(BaseModel):
    attempt_id: int
    question_id: int
    selected_option_id: int

class UserAnswerCreate(UserAnswerBase):
    pass

class UserAnswerResponse(BaseModel):
    Id: int
    attempt_id: int
    question_id: int
    selected_option_id: int = Field(validation_alias="selected_option_Id")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
