from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.role.method import (create_role, delete_role, get_all_roles,
                                     get_role, update_role)
from apps.v1.api.role.schemas import (RoleBase, RoleCreate, RoleResponse,
                                      RoleUpdate)


async def create_role_service(db: AsyncSession, role_data: RoleCreate) -> RoleResponse:
    role = await create_role(db, role_data)
    return RoleResponse.from_orm(role)


async def get_role_service(db: AsyncSession, role_id: int) -> Optional[RoleResponse]:
    role = await get_role(db, role_id)
    if role:
        return RoleResponse.from_orm(role)
    return None

async def get_all_roles_service(db: AsyncSession) -> List[RoleResponse]:
    roles = await get_all_roles(db)
    return [RoleResponse.from_orm(role) for role in roles]

async def update_role_service(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Optional[RoleResponse]:
    role = await update_role(db, role_id, role_data)
    if role:
        return RoleResponse.from_orm(role)
    return None

async def delete_role_service(db: AsyncSession, role_id: int) -> bool:
    return await delete_role(db, role_id)