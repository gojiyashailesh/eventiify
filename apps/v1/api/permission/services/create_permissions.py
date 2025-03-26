from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.create_permission import \
    create_permission
from apps.v1.api.permission.schema import PermissionCreate, PermissionResponse


async def create_permission_service(db: AsyncSession, permission_data: PermissionCreate) -> PermissionResponse:
    permission = await create_permission(db, permission_data)
    return PermissionResponse.from_orm(permission)