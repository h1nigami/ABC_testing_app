from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from ..repositories import TestRepository, QuestionRepository, AnswerOptionRepository
from ..schemas import TestCreate, TestUpdate, QuestionCreate, AnswerOptionCreate

class TestManagementService:
    __test__ = False

    def __init__(self, session: AsyncSession, test_repository: TestRepository, question_repository: QuestionRepository, answer_option_repository: AnswerOptionRepository):
        self._session = session
        self._test_repository = test_repository
        self._question_repository = question_repository
        self._answer_option_repository = answer_option_repository

    async def create_test_with_question(self, test_data: TestCreate, question_data: list[QuestionCreate], author_id: int):
        """Создаёт тест, все его вопросы и варианты ответов в одной транзакции"""
        test = await self._test_repository.create(**test_data.model_dump(), created_by=author_id)
        try:
            for question_d in question_data:
                question_with_test = question_d.model_copy(update={"test_Id": test.Id})
                question = await self._question_repository.create(**question_with_test.model_dump(exclude={"options"}))
                for option in question_d.options:
                    await self._answer_option_repository.create(**option.model_dump(), question_id=question.Id)

            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return await self._test_repository.get_with_details(test.Id)
    
    async def update_test(self, test_id: int, test_data: TestUpdate):
        """Обновляет тест"""
        test = await self._test_repository.get(test_id)
        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
        try:
            await self._test_repository.update(test_id, **test_data.model_dump(exclude_unset=True))
            await self._session.commit()
            return await self._test_repository.get(test_id)
        except Exception as e:
            await self._session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_test(self, test_id: int):
        """Удаляет тест"""
        test = await self._test_repository.get(test_id)
        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
        await self._test_repository.delete(test_id)
        await self._session.commit()

    async def get_test(self, test_id: int):
        """Возвращает тест вместе с вопросами и вариантами ответов"""
        test = await self._test_repository.get_with_details(test_id)
        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
        return test

    async def list_published_tests(self):
        """Список опубликованных тестов"""
        return await self._test_repository.get_all_published()

    async def list_author_tests(self, author_id: int):
        """Список всех тестов автора (включая черновики)"""
        return await self._test_repository.get_by_author(author_id)