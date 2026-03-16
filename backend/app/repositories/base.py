from typing import TypeVar, Type, Optional, List, Dict, Any, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update, delete as sql_delete
from sqlalchemy.orm import class_mapper

ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    async def create(self, **kwargs) -> ModelType:
        instance = self._model(**kwargs)
        self._session.add(instance)
        await self._session.flush()
        return instance
    
    async def delete(self, Id: int) -> None:
        await self._session.execute(sql_delete(self._model).where(self._model.Id == Id))

    async def update(self, Id: int, **kwargs) -> bool:
        stmt = sql_update(self._model).where(self._model.Id == Id).values(**kwargs)
        try:
            await self._session.execute(stmt)
            return True
        except Exception:
            return False
    
    async def list(self) -> List[ModelType]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()
    
    async def get(self, Id: int) -> Optional[ModelType]:
        result = await self._session.execute(select(self._model).where(self._model.Id == Id))
        return result.scalars().first()
    
    async def get_by(self, **kwargs) -> Optional[List[ModelType]]:
        query = select(self._model).where(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().all()
    
    async def to_dict(self, model: ModelType) -> Dict[str, Any]:
        """Преобразование модели в словарь"""
        return {c.key: getattr(model, c.key) for c in class_mapper(model.__class__).mapped_table.c}
    
    async def save(self):
        await self._session.commit()