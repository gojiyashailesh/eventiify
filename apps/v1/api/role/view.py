from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.role.schemas import RoleCreate, RoleResponse, RoleUpdate
from apps.v1.api.role.service import (create_role_service, delete_role_service,
                                      get_all_roles_service, get_role_service,
                                      update_role_service)
from config.db_config import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role_endpoint(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db)
):
    """ route for the role createion"""
    return await create_role_service(db, role_data)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_endpoint(
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """route to get perticular role"""
    role = await get_role_service(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/", response_model=List[RoleResponse])
async def get_all_roles_endpoint(
    db: AsyncSession = Depends(get_db)
):
    """route to get all the role"""
    return await get_all_roles_service(db)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role_endpoint(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """route to update perticular role"""
    role = await update_role_service(db, role_id, role_data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_endpoint(
    role_id: int,
    db: AsyncSession = Depends(get_db)
):
    """route to delete the role"""
    deleted = await delete_role_service(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")