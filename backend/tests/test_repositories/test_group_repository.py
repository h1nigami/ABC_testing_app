import pytest
from app.repositories import GroupRepository, UserRepository
from app.models import User, Group
from typing import List

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