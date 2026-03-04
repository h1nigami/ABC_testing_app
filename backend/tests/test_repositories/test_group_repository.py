import pytest
from app.repositories import GroupRepository

pytestmark = pytest.mark.asyncio

async def test_create_group(session):
    repo = GroupRepository(session=session)
    group = await repo.create(name="test")
    assert group.Id is not None
    assert group.name == "test"

async def test_add_student(session):
    pass