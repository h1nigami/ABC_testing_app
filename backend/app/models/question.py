from ..core.database import Base
from sqlalchemy import Integer, Float, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import List

from enum import Enum as PyEnum

class QuestionType(str, PyEnum):
    SINGLE_CHOISE = "single_choice"
    MULTIPLE_CHOISE = "multiple_choice"

class Question(Base):
    __tablename__ = "question"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_Id: Mapped[int] = mapped_column(ForeignKey("test.Id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    test: Mapped["Test"] = relationship(
        "Test", back_populates="questions"
        )
    options: Mapped[List["AnswerOption"]] = relationship(
        "AnswerOption", back_populates="question", cascade="all, delete-orphan"
    )
    user_answers: Mapped[List["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question(Id={self.Id}, type={self.question_type})>"