from typing import List

from sqlalchemy.future import select

from apps.v1.api.permission.models.methods.create_permission import *


async def get_all_permissions(db: AsyncSession) -> List[Permission]:
    result = await db.execute(select(Permission))
    return result.scalars().all()