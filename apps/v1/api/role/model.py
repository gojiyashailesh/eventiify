"""This module contains database model implementations."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select

from config.db_config import Base


class Role(Base):
    """Table Model of Role

    Args:
        Base (Base):
    """
    __tablename__ = "role"
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    role = Column(String(50),nullable=True)