from .base import BaseRepository
from app.models import Test, Question

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TestRepository(BaseRepository[Test]):
    __test__ = False
    
    def __init__(self, session: AsyncSession):
        super().__init__(Test, session)

    def create(self, **kwargs):
        """
        Параметры
        ---------
        title: str - обязательный\n
        description: str - опциональный\n
        is_published: bool - опциональный\n
        created_by: int - обязательный (айди юзера создавшего тест)\n
        """
        return super().create(**kwargs)
    
    async def get_all_published(self) -> List[Test]:
        query = select(self._model).where(self._model.is_published == True)
        result = await self._session.execute(query)
        return result.scalars().all()
    