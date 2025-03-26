from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.delete_permission import \
    delete_permission


async def delete_permission_service(db: AsyncSession, permission_id: int) -> bool:
    return await delete_permission(db, permission_id)