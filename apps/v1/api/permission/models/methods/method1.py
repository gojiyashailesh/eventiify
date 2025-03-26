from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.model import Permission
from apps.v1.api.permission.schema import (PermissionBase, PermissionCreate,
                                           PermissionResponse,
                                           PermissionUpdate)
from core.db.mixins.save_to_db import save_object


async def create_permission(db: AsyncSession, permission_data: PermissionCreate) -> Permission:
    new_permission = Permission(permission=permission_data.permission)
    return await save_object(db, new_permission)