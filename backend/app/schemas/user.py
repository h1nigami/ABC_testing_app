from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    login: str = Field(..., min_length=6, max_length=32)
    role: str = "student"   
    group_id: Optional[int] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32)

class UserUpdate(BaseModel):
    login: Optional[str] = Field(..., min_length=6, max_length=32)
    password: Optional[str] = Field(..., min_length=8, max_length=32)
    role: Optional[str] = None
    group_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)