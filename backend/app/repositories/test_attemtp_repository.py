from .base import BaseRepository
from app.models import TestAttempt
from sqlalchemy.ext.asyncio import AsyncSession

class TestAttemptRepository(BaseRepository[TestAttempt]):
    __test__ = False

    def __init__(self, session: AsyncSession):
        super().__init__(TestAttempt ,session)