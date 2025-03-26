"""Permission Table Schemas"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select

from config.db_config import Base


class Permission (Base):
    """Permission Table Schemas"""
    __tablename__ = "permission"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    permission = Column(String(100),nullable=False)