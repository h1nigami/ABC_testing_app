from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TestAttemptBase(BaseModel):
    __test__ = False

    test_id: int

class TestAttemptCreate(TestAttemptBase):
    pass

class TestAttemptUpdate(BaseModel):
    __test__ = False

    finished_at: Optional[datetime] = None
    score: Optional[float] = None

class TestAttemptResponse(TestAttemptBase):
    Id: int
    user_id: int
    started_at: int
    finished_at: Optional[datetime] = None
    score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)