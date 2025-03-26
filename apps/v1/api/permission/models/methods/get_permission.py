from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.v1.api.permission.models.model import Permission
from apps.v1.api.permission.schema import PermissionBase


async def get_permission(db: AsyncSession, permission_id: int) -> Optional[Permission]:
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    return result.scalar_one_or_none()