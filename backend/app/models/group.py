from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..core.database import Base

class Group(Base):
    __tablename__ = "group"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    awailable_tests: Mapped[int] = mapped_column(ForeignKey("test.Id", use_alter=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    students: Mapped[list["User"]] = relationship(
        "User", back_populates="group", cascade="all, delete-orphan"
    )