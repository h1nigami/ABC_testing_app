from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    awailable_tests: Optional[int] = None

class GroupResponse(GroupBase):
    Id: int
    awailable_tests: Optional[int] = None
    created_at: datetime
    updated_at: datetime