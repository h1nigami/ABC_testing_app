from ..core.database import Base

from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserAnswer(Base):
    __tablename__ = "user_answer"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("test_attempt.Id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.Id"), nullable=False)
    selected_option_Id: Mapped[int] = mapped_column(
        ForeignKey("answer_option.Id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    attempt: Mapped["TestAttempt"] = relationship("TestAttempt", back_populates="user_answers")
    question: Mapped["Question"] = relationship("Question", back_populates="user_answers")
    selected_option: Mapped["AnswerOption"] = relationship("AnswerOption", back_populates="user_answers")

    def __repr__(self):
        return f"<UserAnswer(Id={self.Id}, attempt_Id={self.attempt_id}, option_Id={self.selected_option_Id})>"
