from .base import BaseRepository
from app.models import Test, Question

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TestRepository(BaseRepository[Test]):
    def __init__(self, session: AsyncSession):
        super().__init__(Test, session)
    
    async def get_all_published(self) -> List[Test]:
        query = select(self._model).where(self._model.is_published == True)
        result = await self._session.execute(query)
        return result.scalars().all()
    