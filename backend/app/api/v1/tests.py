from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from ...schemas import (
    TestCreate,
    TestUpdate,
    TestResponse,
    QuestionCreate,
    TestPublic,
)
from ...core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ...factory import ServiceFactory

qwiz_router = APIRouter(prefix="/api/test", tags=["tests"])


@qwiz_router.post(path="/create", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
async def make_test(
    test_data: TestCreate,
    questions: list[QuestionCreate],
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    test = await service.create_test_with_question(test_data=test_data, question_data=questions, author_id=author_id)
    return TestResponse.model_validate(test)


@qwiz_router.get(path="/", response_model=list[TestResponse])
async def list_published_tests(db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    tests = await service.list_published_tests()
    return [TestResponse.model_validate(t) for t in tests]


@qwiz_router.get(path="/{test_id}", response_model=TestResponse)
async def get_test(test_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    test = await service.get_test(test_id)
    return TestResponse.model_validate(test)


@qwiz_router.get(path="/{test_id}/take", response_model=TestPublic)
async def take_test(test_id: int, db: AsyncSession = Depends(get_db)):
    """Версия теста для прохождения — без пометок о правильных вариантах."""
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    test = await service.get_test(test_id)
    if not test.is_published:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Test is not published")
    return TestPublic.model_validate(test)


@qwiz_router.patch(path="/{test_id}", response_model=TestResponse)
async def update_test(test_id: int, test_data: TestUpdate, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    await service.update_test(test_id, test_data)
    test = await service.get_test(test_id)
    return TestResponse.model_validate(test)


@qwiz_router.post(path="/{test_id}/publish", response_model=TestResponse)
async def publish_test(test_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    await service.update_test(test_id, TestUpdate(is_published=True))
    test = await service.get_test(test_id)
    return TestResponse.model_validate(test)


@qwiz_router.delete(path="/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(test_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    await service.delete_test(test_id)
    return None
