import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app as fastapi_app
from app.core.database import Base, get_db

API_TEST_DSN = "sqlite+aiosqlite:///test_api.db"


@pytest_asyncio.fixture
async def api_engine():
    engine = create_async_engine(
        API_TEST_DSN,
        poolclass=NullPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client(api_engine):
    TestSession = async_sessionmaker(
        bind=api_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            await db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()
