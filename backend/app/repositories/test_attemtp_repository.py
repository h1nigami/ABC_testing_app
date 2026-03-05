from .base import BaseRepository
from app.models import TestAttempt
from sqlalchemy.ext.asyncio import AsyncSession

class TestAttemptRepository(BaseRepository[TestAttempt]):
    def __init__(self, model, session: AsyncSession):
        super().__init__(TestAttempt ,session)