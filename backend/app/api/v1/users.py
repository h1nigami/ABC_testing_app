from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas import UserCreate, UserResponse, UserLogin
from ...core.database import get_db
from ...factory import ServiceFactory

users_router = APIRouter(prefix="/api/users", tags=["users"])


@users_router.post(path="/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_user_service()
    user = await service.register(user_data)
    return UserResponse.model_validate(user)


@users_router.post(path="/login", response_model=UserResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_user_service()
    user = await service.authenticate(credentials.login, credentials.password)
    return UserResponse.model_validate(user)


@users_router.get(path="/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_user_service()
    user = await service.get_user(user_id)
    return UserResponse.model_validate(user)
