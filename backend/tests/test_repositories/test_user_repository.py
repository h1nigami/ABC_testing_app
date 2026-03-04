import pytest
from app.repositories import UserRepository, GroupRepository

pytestmark = pytest.mark.asyncio

async def test_create_user(session):
    repo = UserRepository(session=session)
    user = await repo.create(login="test", password="test")
    assert user.Id is not None
    assert user.login == "test"


async def test_get_user(session):
    repo = UserRepository(session=session)
    user = await repo.create(login="test1", password="test")
    retrieved_user = await repo.get(user.Id)
    assert retrieved_user.Id == user.Id
    assert retrieved_user.login == user.login

async def test_delete_user(session):
    repo = UserRepository(session=session)
    user = await repo.create(login="test2", password="test")
    await repo.delete(user.Id)
    retrieved_user = await repo.get(user.Id)
    assert retrieved_user is None

async def test_get_user_by_login(session):
    repo = UserRepository(session=session)
    user = await repo.create(login="test3", password="test")
    retrieved_user = await repo.get_by_login(user.login)
    assert retrieved_user.Id is not None
    assert retrieved_user.Id == user.Id
    assert retrieved_user.login == user.login

async def test_update_user(session):
    repo = UserRepository(session=session)
    user = await repo.create(login="test4", password="test")
    await repo.update(user.Id, login="test4_updated")
    retrieved_user = await repo.get(user.Id)
    assert retrieved_user.Id is not None
    assert retrieved_user.Id == user.Id
    assert retrieved_user.login == "test4_updated"

async def test_list_users(session):
    repo = UserRepository(session=session)
    await repo.create(login="test5", password="test")
    await repo.create(login="test6", password="test")
    users = await repo.list()
    assert len(users) > 0
    assert users[0].login == "test"
    assert users[-1].login == "test6"

async def test_user_add_to_group(session):
    user_repo = UserRepository(session=session)
    group_repo = GroupRepository(session=session)
    user = await user_repo.create(login="test7", password="test")
    group = await group_repo.create(name="test_group")
    await user_repo.add_to_group(user, group.Id)
    assert user.group_id == group.Id