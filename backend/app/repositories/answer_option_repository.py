from app.models import AnswerOption
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository

class AnswerOptionRepository(BaseRepository[AnswerOption]):
    def __init__(self, session: AsyncSession):
        super().__init__(AnswerOption, session)