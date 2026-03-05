from sqlalchemy import ForeignKey, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from ..core.database import Base

from typing import Optional, List

class TestAttempt(Base):
    __tablename__ = "test_attempt"
    __test__ = False

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("test.Id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.Id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    score: Mapped[Optional[float]] = mapped_column(Float)

    test: Mapped["Test"] = relationship("Test", back_populates="attempts")
    user: Mapped["User"] = relationship("User", back_populates="test_attempts")
    user_answers: Mapped[List["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="attempt", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<TestAttempt(id={self.id}, user_id={self.user_id}, test_id={self.test_id})>"