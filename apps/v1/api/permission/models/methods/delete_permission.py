from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.models.methods.get_permission import get_permission


async def delete_permission(db: AsyncSession, permission_id: int) -> bool:
    permission = await get_permission(db, permission_id)
    if permission:
        await db.delete(permission)
        await db.commit()
        return True
    return False