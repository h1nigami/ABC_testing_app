import datetime

from ..core.database import Base

from enum import Enum as PyEnum
from typing import List

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

class UserRole(str, PyEnum):
    STUDENT = "student"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "user"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.Id"), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    created_tests: Mapped[List["Test"]] = relationship(
        "Test", back_populates="creator", cascade="all, delete-orphan"
    )
    test_attempts: Mapped[List["TestAttempt"]] = relationship(
        "TestAttempt", back_populates="user", cascade="all, delete-orphan"
    )
    group: Mapped["Group"] = relationship(
        "Group", back_populates="students"
    )
    def __repr__(self):
        return f"<User(id={self.Id}, login={self.login}, role={self.role})>"

