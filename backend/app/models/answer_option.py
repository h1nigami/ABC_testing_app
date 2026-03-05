from ..core.database import Base

from typing import List

from sqlalchemy import Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class AnswerOption(Base):
    __tablename__ = "answer_option"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.Id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    question: Mapped["Question"] = relationship("Question", back_populates="options")
    user_answers: Mapped[List["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="selected_option"
    )

    def __repr__(self):
        return f"<AnswerOption(id={self.Id}, is_correct={self.is_correct})>"