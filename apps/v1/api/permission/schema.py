from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ValidationError

from apps.v1.api.client.models import attribute
from core.utils import helper


class PermissionBase(BaseModel):
    """Validation for PErmidsion table"""
    permission :Optional[str]=None
    
class PermissionCreate(PermissionBase):
    """create the permission"""
    pass

class PermissionUpdate(PermissionBase):
    """update permission"""
    pass

class PermissionResponse(PermissionBase):
    """Permission response"""
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True