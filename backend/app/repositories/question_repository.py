from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Question
from .base import BaseRepository

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)

    async def create(self, **kwargs):
        """
        Параметры
        ---------
        test_Id: int - обязательный\n
        text: str - обязательный\n
        question_type: str - обязательный (single_choice/multiple_choice)\n
        order_index: int - обязательный (порядковый номер вопроса)\n
        points: float - обязательный (по дефолту 1.0)\n
        """
        return await super().create(**kwargs)