from fastapi.routing import APIRouter
from fastapi import Depends, status, Query
from ...schemas import (
    TestCreate,
    TestBase,
    TestUpdate,
    TestResponse,
    QuestionBase,
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    AnswerOptionBase,
    AnswerOptionCreate,
    AnswerOptionResponse,
    AnswerOptionUpdate
)
from ...services import TestingService, TestManagementService
from ...core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ...factory import ServiceFactory

qwiz_router = APIRouter(prefix="/api/test", tags=["tests"])

@qwiz_router.post(path="/create", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
async def make_test(
    test_data: TestCreate,
    questions: list[QuestionCreate],
    author_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    factory = ServiceFactory(session=db)
    service = factory.get_management_service()
    test = await service.create_test_with_question(test_data=test_data, question_data=questions, author_id=author_id)
    response = TestResponse.model_validate(test)
    return response

