from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import  AsyncSession, create_async_engine, async_sessionmaker
import os

from .config import load_env

load_env()

DSN = os.getenv("DSN")

engine = create_async_engine(DSN)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

Base = declarative_base()

async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        await db.close()