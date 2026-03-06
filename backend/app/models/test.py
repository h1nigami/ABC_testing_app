from ..core.database import Base
from datetime import datetime

from typing import Optional, List

from sqlalchemy import DateTime, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Test(Base):
    __tablename__ = "test"

    __test__ = False

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey("user.Id"), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    creator: Mapped["User"] = relationship("User", back_populates="created_tests")
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="test", cascade="all, delete-orphan"
    )
    attempts: Mapped[List["TestAttempt"]] = relationship(
        "TestAttempt", back_populates="test", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Test(Id={self.Id}, title={self.title})>"