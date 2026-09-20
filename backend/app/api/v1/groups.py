from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas import GroupCreate, GroupResponse, UserResponse
from ...core.database import get_db
from ...factory import ServiceFactory

groups_router = APIRouter(prefix="/api/group", tags=["groups"])


@groups_router.post(path="/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(group_data: GroupCreate, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_group_service()
    group = await service.create_group(group_data)
    return GroupResponse.model_validate(group)


@groups_router.get(path="/{group_id}", response_model=GroupResponse)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_group_service()
    group = await service.get_group(group_id)
    return GroupResponse.model_validate(group)


@groups_router.post(path="/{group_id}/students/{user_id}", response_model=UserResponse)
async def add_student(group_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_group_service()
    user = await service.add_student(group_id, user_id)
    return UserResponse.model_validate(user)


@groups_router.get(path="/{group_id}/students", response_model=list[UserResponse])
async def list_students(group_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_group_service()
    students = await service.list_students(group_id)
    return [UserResponse.model_validate(s) for s in students]
