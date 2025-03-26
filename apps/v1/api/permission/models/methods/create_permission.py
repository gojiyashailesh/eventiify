from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.model import Permission
from apps.v1.api.permission.schema import PermissionBase
from core.db.mixins.save_to_db import save_object


async def create_permission(db:AsyncSession,permission_data:PermissionBase)->Optional[Permission]:
    """create_permission"""
    try:
        new_permission = Permission(permission = permission_data.permission)
        return await save_object(db,new_permission)
    except Exception as e:
        await db.rollback()
        print(f"Error{e}")
        return None