import datetime

from ..core.database import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    Id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    fullName = Column(String)
    password = Column(String)
    role = Column(String, default="student")
    group_id = Column(Integer, ForeignKey("groups.Id"), nullable=True) 
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now())
