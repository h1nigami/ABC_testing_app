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
from app.services import (
    TestingService,
    TestManagementService,
    UserService,
    GroupService,
)


class ServiceFactory:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._test_repo = None
        self._question_repo = None
        self._answer_option_repo = None
        self._test_attempt_repo = None
        self._user_answer_repo = None
        self._user_repo = None
        self._group_repo = None

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

    @property
    def test_attempt_repository(self) -> TestAttemptRepository:
        if not self._test_attempt_repo:
            self._test_attempt_repo = TestAttemptRepository(session=self._session)
        return self._test_attempt_repo

    @property
    def user_answer_repository(self) -> UserAnswerRepository:
        if not self._user_answer_repo:
            self._user_answer_repo = UserAnswerRepository(session=self._session)
        return self._user_answer_repo

    @property
    def user_repository(self) -> UserRepository:
        if not self._user_repo:
            self._user_repo = UserRepository(session=self._session)
        return self._user_repo

    @property
    def group_repository(self) -> GroupRepository:
        if not self._group_repo:
            self._group_repo = GroupRepository(session=self._session)
        return self._group_repo

    def get_management_service(self) -> TestManagementService:
        return TestManagementService(
            session=self._session,
            test_repository=self.test_repository,
            question_repository=self.question_repository,
            answer_option_repository=self.answer_option_repository
        )

    def get_testing_service(self) -> TestingService:
        return TestingService(
            session=self._session,
            test_attempt_repository=self.test_attempt_repository,
            user_answer_repository=self.user_answer_repository,
            question_repository=self.question_repository,
            answer_option_repository=self.answer_option_repository,
        )

    def get_user_service(self) -> UserService:
        return UserService(
            session=self._session,
            user_repository=self.user_repository,
        )

    def get_group_service(self) -> GroupService:
        return GroupService(
            session=self._session,
            group_repository=self.group_repository,
            user_repository=self.user_repository,
        )
