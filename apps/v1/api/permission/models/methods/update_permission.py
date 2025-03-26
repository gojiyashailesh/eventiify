from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.get_permission import get_permission
from apps.v1.api.permission.models.model import Permission
from apps.v1.api.permission.schema import PermissionUpdate
from core.db.mixins.save_to_db import save_object


async def update_permission(db: AsyncSession, permission_id: int, permission_data: PermissionUpdate) -> Optional[Permission]:
    permission = await get_permission(db, permission_id)
    if permission:
        update_data = permission_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(permission, key, value)
        return await save_object(db, permission)
    return None