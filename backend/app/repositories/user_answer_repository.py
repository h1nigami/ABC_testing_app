from .base import BaseRepository
from app.models import UserAnswer
from sqlalchemy.ext.asyncio import AsyncSession

class UserAnswerRepository(BaseRepository[UserAnswer]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserAnswer, session)