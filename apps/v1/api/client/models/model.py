"""This module contains database model implementations."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, LargeBinary, Boolean, Enum, ForeignKey, func, Date

from sqlalchemy import event
from config.db_config import Base
from apps.v1.api.client.models import attribute
from core.utils import helper
    
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    phone_no = Column(String(10), nullable=False, unique=True)
    gender = Column(Enum(attribute.Gender), nullable=False)
    profile_image = Column(LargeBinary, nullable=True)
    status = Column(Boolean, nullable=False, default=1)
    role_permission_id = Column(Integer, ForeignKey('role_permission.id'), nullable=False)
    last_login_time = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey('admin.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=helper.DateTimeUtils.get_time)
    deleted_at = Column(DateTime, nullable=True)
    
