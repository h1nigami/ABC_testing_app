from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List

from ..repositories import GroupRepository, UserRepository
from ..schemas import GroupCreate
from ..models import Group, User


class GroupService:
    """Управление учебными группами и составом учеников."""

    def __init__(self, session: AsyncSession, group_repository: GroupRepository, user_repository: UserRepository):
        self._session = session
        self._group_repository = group_repository
        self._user_repository = user_repository

    async def create_group(self, group_data: GroupCreate) -> Group:
        try:
            group = await self._group_repository.create(**group_data.model_dump())
            await self._session.commit()
            return group
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_group(self, group_id: int) -> Group:
        group = await self._group_repository.get(group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return group

    async def add_student(self, group_id: int, user_id: int) -> User:
        group = await self._group_repository.get(group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        user = await self._user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self._user_repository.add_to_group(user, group_id)
        await self._session.commit()
        return await self._user_repository.get(user_id)

    async def list_students(self, group_id: int) -> List[User]:
        group = await self._group_repository.get(group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return await self._group_repository.list_students(group)
