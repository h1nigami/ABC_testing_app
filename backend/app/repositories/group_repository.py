from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from app.models import Group, User

from .base import BaseRepository

class GroupRepository(BaseRepository[Group]):
    def __init__(self, session: AsyncSession):
        super().__init__(Group, session)

    async def get_by_name(self, name: str) -> Group:
        result = await self._session.execute(select(self._model).where(self._model.name == name))
        return result.scalar()
    
    async def list_students(self, group: Group) -> list[User]:
        query = select(User).join(Group).where(User.group_id == group.id)
        result = await self._session.execute(query)
        return result.scalars().all()
