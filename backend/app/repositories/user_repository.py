from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update
from app.models import User

from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_login(self, login: str) -> User:
        result = await self._session.execute(select(self._model).where(self._model.login == login))
        return result.scalar()
    
    async def add_to_group(self, user: User, group_id: int) -> None:
        await self._session.execute(sql_update(self._model)
                                    .where(self._model.Id == user.Id)
                                    .values(group_id=group_id))
