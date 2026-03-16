import pytest
from app.services import TestManagementService
from app.repositories import *
from app.schemas import QuestionCreate, TestCreate, AnswerOptionCreate
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

pytestmark = pytest.mark.asyncio

async def test_create_test(session: AsyncSession):
    ts = TestManagementService(
        session=session,
        test_repository=TestRepository(session=session),
        answer_option_repository=AnswerOptionRepository(session=session),
        question_repository=QuestionRepository(session=session),
    )
    new_test = TestCreate(title=str(uuid.uuid4()), description=str(uuid.uuid4()))
    options = [AnswerOptionCreate(text=str(uuid.uuid4()), is_correct=True, order_index=1)]
    questions = [QuestionCreate(text=str(uuid.uuid4()), question_type="single_choice", options=options)]
    
    test = await ts.create_test_with_question(new_test, questions, 1)
    
    assert isinstance(test, ts._test_repository._model)
    result = await session.execute(
        select(ts._question_repository._model).where(ts._question_repository._model.test_Id == test.Id)
    )
    db_questions = result.scalars().all()
    
    assert len(db_questions) == 1
    assert db_questions[0].text == questions[0].text
    