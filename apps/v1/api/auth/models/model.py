"""This module contains database model implementations."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, LargeBinary, Boolean, Enum, ForeignKey, func, Date
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy import event
from config.db_config import Base
import enum


class gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    phone_no = Column(String(10), nullable=False, unique=True)
    gender = Column(Enum(gender), nullable=False)
    profile_image = Column(LargeBinary, nullable=True)
    status = Column(Boolean, nullable=False, default=1)
    last_login_time = Column(DateTime, nullable=True)
    role_permission_id = Column(Integer, ForeignKey('role_permission.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    phone_no = Column(String(10), nullable=False, unique=True)
    profile_image = Column(LargeBinary, nullable=True)
    status = Column(Boolean, nullable=False, default=1)
    last_login_time = Column(DateTime, nullable=True)
    dob = Column(DateTime, nullable=False)
    gender = Column(Enum(gender), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
