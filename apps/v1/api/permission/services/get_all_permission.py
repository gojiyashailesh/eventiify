from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.get_all_permission import \
    get_all_permissions
from apps.v1.api.permission.schema import PermissionResponse


async def get_all_permissions_service(db: AsyncSession) -> List[PermissionResponse]:
    permissions = await get_all_permissions(db)
    return [PermissionResponse.from_orm(permission) for permission in permissions]