from ..repositories import TestAttemptRepository, UserAnswerRepository, QuestionRepository, AnswerOptionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..schemas import UserAnswerCreate
from ..models import Question, TestAttempt
from datetime import datetime


class TestingService:
    """Сервис прохождения теста учеником: старт попытки, ответы, завершение и подсчёт баллов."""

    def __init__(self, session: AsyncSession, test_attempt_repository: TestAttemptRepository, user_answer_repository: UserAnswerRepository, question_repository: QuestionRepository, answer_option_repository: AnswerOptionRepository):
        self._session = session
        self._test_attempt_repository = test_attempt_repository
        self._user_answer_repository = user_answer_repository
        self._question_repository = question_repository
        self._answer_option_repository = answer_option_repository

    async def get_attempt(self, attempt_id: int) -> TestAttempt:
        attempt = await self._test_attempt_repository.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test attempt not found")
        return attempt

    async def start_attempt(self, user_id: int, test_id: int) -> TestAttempt:
        try:
            test_attempt = await self._test_attempt_repository.create(test_id=test_id, user_id=user_id)
            await self._session.commit()
            return test_attempt
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def submit_answer(self, attempt_id: int, answer_data: UserAnswerCreate):
        attempt = await self._test_attempt_repository.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test attempt not found")
        if attempt.finished_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test attempt already finished")

        question = await self._question_repository.get(answer_data.question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

        answer = await self._user_answer_repository.create(
            attempt_id=attempt_id,
            question_id=answer_data.question_id,
            selected_option_Id=answer_data.selected_option_id,
        )
        await self._session.commit()
        return answer

    async def finish_attempt(self, attempt_id: int) -> TestAttempt:
        attempt = await self._test_attempt_repository.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test attempt not found")
        if attempt.finished_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test attempt already finished")

        answers = await self._user_answer_repository.get_by(attempt_id=attempt_id)

        # Группируем выбранные варианты по вопросу
        selected_by_question: dict[int, set[int]] = {}
        for ans in answers:
            selected_by_question.setdefault(ans.question_id, set()).add(ans.selected_option_Id)

        total_score = 0.0
        for question_id, selected_ids in selected_by_question.items():
            question = await self._question_repository.get(question_id)
            if not question:
                continue
            correct_options = await self._answer_option_repository.get_by(
                question_id=question_id, is_correct=True
            )
            correct_ids = {option.Id for option in correct_options}
            if not correct_ids:
                continue
            if question.question_type == "single_choice":
                # один выбранный вариант, и он должен быть верным
                if len(selected_ids) == 1 and selected_ids.issubset(correct_ids):
                    total_score += question.points
            else:  # multiple_choice — нужно выбрать ровно все верные варианты
                if selected_ids == correct_ids:
                    total_score += question.points

        await self._test_attempt_repository.update(
            attempt_id,
            finished_at=datetime.now(),
            score=total_score,
        )
        await self._session.commit()
        return await self._test_attempt_repository.get(attempt_id)
