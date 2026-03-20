from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import (
    AnswerOptionRepository,
    GroupRepository,
    QuestionRepository,
    TestAttemptRepository,
    TestRepository,
    UserRepository,
    UserAnswerRepository
)
from app.services import TestingService, TestManagementService

class ServiceFactory:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._test_repo = None
        self._question_repo = None
        self._answer_option_repo = None

    @property
    def test_repository(self) -> TestRepository:
        if not self._test_repo:
            self._test_repo = TestRepository(session=self._session)
        return self._test_repo
    
    @property
    def question_repository(self) -> QuestionRepository:
        if not self._question_repo:
            self._question_repo = QuestionRepository(session=self._session)
        return self._question_repo
    
    @property
    def answer_option_repository(self) -> AnswerOptionRepository:
        if not self._answer_option_repo:
            self._answer_option_repo = AnswerOptionRepository(session=self._session)
        return self._answer_option_repo
    
    def get_management_service(self) -> TestManagementService:
        return TestManagementService(
            session=self._session,
            test_repository=self.test_repository,
            question_repository=self.question_repository,
            answer_option_repository=self.answer_option_repository
        )
