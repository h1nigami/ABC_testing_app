import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.factory import ServiceFactory
from app.repositories import UserRepository
from app.schemas import TestCreate, QuestionCreate, AnswerOptionCreate, UserAnswerCreate

pytestmark = pytest.mark.asyncio


async def _make_test_with_question(factory: ServiceFactory, author_id: int, question_type: str, options):
    mgmt = factory.get_management_service()
    test_data = TestCreate(title=str(uuid.uuid4()))
    question = QuestionCreate(
        text=str(uuid.uuid4()),
        question_type=question_type,
        order_index=1,
        points=3.0,
        options=[AnswerOptionCreate(**o) for o in options],
    )
    test = await mgmt.create_test_with_question(test_data, [question], author_id)
    return test


async def test_multiple_choice_exact_match_scores_points(session: AsyncSession):
    factory = ServiceFactory(session=session)
    user = await UserRepository(session=session).create(login="mc_user_ok", password="x")
    await session.commit()

    test = await _make_test_with_question(
        factory,
        user.Id,
        "multiple_choice",
        [
            {"text": "A", "is_correct": True, "order_index": 1},
            {"text": "B", "is_correct": True, "order_index": 2},
            {"text": "C", "is_correct": False, "order_index": 3},
        ],
    )
    question = test.questions[0]
    correct_ids = [o.Id for o in question.options if o.is_correct]

    testing = factory.get_testing_service()
    attempt = await testing.start_attempt(user_id=user.Id, test_id=test.Id)
    for option_id in correct_ids:
        await testing.submit_answer(
            attempt.Id,
            UserAnswerCreate(attempt_id=attempt.Id, question_id=question.Id, selected_option_id=option_id),
        )

    finished = await testing.finish_attempt(attempt.Id)
    assert finished.score == 3.0


async def test_multiple_choice_partial_selection_scores_zero(session: AsyncSession):
    factory = ServiceFactory(session=session)
    user = await UserRepository(session=session).create(login="mc_user_bad", password="x")
    await session.commit()

    test = await _make_test_with_question(
        factory,
        user.Id,
        "multiple_choice",
        [
            {"text": "A", "is_correct": True, "order_index": 1},
            {"text": "B", "is_correct": True, "order_index": 2},
            {"text": "C", "is_correct": False, "order_index": 3},
        ],
    )
    question = test.questions[0]
    one_correct = next(o.Id for o in question.options if o.is_correct)

    testing = factory.get_testing_service()
    attempt = await testing.start_attempt(user_id=user.Id, test_id=test.Id)
    await testing.submit_answer(
        attempt.Id,
        UserAnswerCreate(attempt_id=attempt.Id, question_id=question.Id, selected_option_id=one_correct),
    )

    finished = await testing.finish_attempt(attempt.Id)
    assert finished.score == 0.0
