from fastapi import FastAPI
from app.repositories import (
    AnswerOptionRepository,
    GroupRepository,
    QuestionRepository,
    TestAttemptRepository,
    TestRepository,
    UserAnswerRepository,
    UserRepository
)

answer_option_repository = AnswerOptionRepository()
group_repository = GroupRepository()
question_repository = QuestionRepository()
test_attempt_repository = TestAttemptRepository()
test_repository = TestRepository()


app = FastAPI(debug=True)

