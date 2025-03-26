from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.update_permission import \
    update_permission
from apps.v1.api.permission.schema import PermissionResponse, PermissionUpdate


async def update_permission_service(db: AsyncSession, permission_id: int, permission_data: PermissionUpdate) -> Optional[PermissionResponse]:
    permission = await update_permission(db, permission_id, permission_data)
    if permission:
        return PermissionResponse.from_orm(permission)
    return None