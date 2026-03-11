from ..repositories import TestAttemptRepository, UserAnswerRepository, QuestionRepository, AnswerOptionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..schemas import UserAnswerCreate
from datetime import datetime

class TestingService:
    def __init__(self, session: AsyncSession, test_attempt_repository: TestAttemptRepository, user_answer_repository: UserAnswerRepository, question_repository: QuestionRepository, answer_option_repository: AnswerOptionRepository):
        self._session = session
        self._test_attempt_repository = test_attempt_repository
        self._user_answer_repository = user_answer_repository
        self._question_repository = question_repository
        self._answer_option_repository = answer_option_repository

    async def start_attempt(self, user_id: int, test_id: int):
        try:
            test_attempt = await self._test_attempt_repository.create(test_id=test_id, user_id=user_id)
            return test_attempt
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def submit_answer(self, attempt_id: int, answer_data: UserAnswerCreate):
        attempt = await self._test_attempt_repository.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test attempt not found")
        if attempt.finished_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test attempt already finished")
        
        answer = await self._user_answer_repository.create(**answer_data.model_dump())
        return answer
    
    async def finish_attempt(self, attempt_id: int):
        attempt = await self._test_attempt_repository.get(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test attempt not found")
        if attempt.finished_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test attempt already finished")
        
        answers = await self._user_answer_repository.get_by(attempt_id=attempt_id)

        total_score = 0
        for ans in answers:
            question = await self._question_repository.get(ans.question_id)
            if question.question_type == "single_choice":
                selected = await self._answer_option_repository.get(ans.selected_option_Id)
                if selected in selected.is_correct:
                    total_score += question.points
        attempt = await self._test_attempt_repository.update(
            attempt_id,
            finished_at=datetime.now(),
            total_score=total_score
        )
        return attempt
