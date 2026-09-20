from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..repositories import UserRepository
from ..schemas import UserCreate
from ..core.security import Security
from ..models import User


class UserService:
    """Регистрация и аутентификация пользователей."""

    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self._session = session
        self._user_repository = user_repository

    async def register(self, user_data: UserCreate) -> User:
        existing = await self._user_repository.get_by_login(user_data.login)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this login already exists",
            )
        try:
            user = await self._user_repository.create(
                login=user_data.login,
                password=Security.hash_password(user_data.password),
                role=user_data.role,
                group_id=user_data.group_id,
            )
            await self._session.commit()
            return user
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def authenticate(self, login: str, password: str) -> User:
        user = await self._user_repository.get_by_login(login)
        if not user or not Security.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login or password",
            )
        return user

    async def get_user(self, user_id: int) -> User:
        user = await self._user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
