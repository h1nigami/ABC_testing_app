from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas import (
    TestAttemptCreate,
    TestAttemptResponse,
    UserAnswerCreate,
    UserAnswerResponse,
)
from ...core.database import get_db
from ...factory import ServiceFactory

attempts_router = APIRouter(prefix="/api/attempt", tags=["attempts"])


@attempts_router.post(path="/start", response_model=TestAttemptResponse, status_code=status.HTTP_201_CREATED)
async def start_attempt(attempt_data: TestAttemptCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_testing_service()
    attempt = await service.start_attempt(user_id=user_id, test_id=attempt_data.test_id)
    return TestAttemptResponse.model_validate(attempt)


@attempts_router.post(path="/{attempt_id}/answer", response_model=UserAnswerResponse, status_code=status.HTTP_201_CREATED)
async def submit_answer(attempt_id: int, answer_data: UserAnswerCreate, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_testing_service()
    answer = await service.submit_answer(attempt_id=attempt_id, answer_data=answer_data)
    return UserAnswerResponse.model_validate(answer)


@attempts_router.post(path="/{attempt_id}/finish", response_model=TestAttemptResponse)
async def finish_attempt(attempt_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_testing_service()
    attempt = await service.finish_attempt(attempt_id=attempt_id)
    return TestAttemptResponse.model_validate(attempt)


@attempts_router.get(path="/{attempt_id}", response_model=TestAttemptResponse)
async def get_attempt(attempt_id: int, db: AsyncSession = Depends(get_db)):
    factory = ServiceFactory(session=db)
    service = factory.get_testing_service()
    attempt = await service.get_attempt(attempt_id)
    return TestAttemptResponse.model_validate(attempt)
