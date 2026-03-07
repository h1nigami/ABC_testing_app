import pytest
from app.repositories import GroupRepository, UserRepository, TestRepository, QuestionRepository
from app.models import User, Group
from typing import List

import uuid

pytestmark = pytest.mark.asyncio

async def test_create_group(session):
    repo = GroupRepository(session=session)
    group = await repo.create(name="test")
    await repo.save()
    assert group is not None
    assert group.name == "test"

async def test_list_student_in_group(session):
    repo = GroupRepository(session=session)
    group = await repo.get(1)
    students = await repo.list_students(group=group)
    assert isinstance(students, list)
    assert all(isinstance(u, User) for u in students)
    user_repo = UserRepository(session=session)
    student = await user_repo.create(login="test10",password="test10")
    await user_repo.save()
    assert student is not None
    await user_repo.add_to_group(student, 1)
    students = await repo.list_students(group=group)
    assert len(students) > 0
    assert students[0].Id == student.Id

async def test_get_awailable_tests(session):
    test_repo = TestRepository(session=session)
    question_repo = QuestionRepository(session=session)
    group_repo = GroupRepository(session=session)
    user_repo = UserRepository(session=session)
    user = await user_repo.create(login="test11",password="test11")
    await user_repo.save()
    group = await group_repo.create(name="группа1")
    test = await test_repo.create(title="тест1", created_by=user.Id)
    await test_repo.save()
    question = await question_repo.create(test_Id=test.Id, text="ответ1", question_type="single_choice", order_index=1, points=1.0)
    await test_repo.add_question(test=test, question=question)
    list_questions = await test_repo.get_questions(test=test)
    assert len(list_questions) > 0

    