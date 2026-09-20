from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.models  # noqa: F401  # регистрируем модели в метаданных
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте (для локальной разработки; в проде — миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="ABC Testing App",
    description="Платформа для создания и прохождения тестов",
    version="1.0.0",
    debug=True,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["health"])
async def root():
    return {"name": "ABC Testing App", "status": "ok"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}
