from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.permission.schema import (PermissionBase, PermissionCreate,
                                           PermissionResponse,
                                           PermissionUpdate)
from apps.v1.api.permission.services.create_permissions import \
    create_permission_service
from apps.v1.api.permission.services.delete_permission_service import \
    delete_permission_service
from apps.v1.api.permission.services.get_all_permission import \
    get_all_permissions_service
from apps.v1.api.permission.services.get_permission_service import \
    get_permission
from apps.v1.api.permission.services.update_permission import \
    update_permission_service
from config.db_config import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission_endpoint(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_permission_service(db, permission_data)

@router.get("/", response_model=List[PermissionResponse])
async def get_all_permissions_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_permissions_service(db)

@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission_endpoint(
    permission_id: int,
    db: AsyncSession = Depends(get_db)
):
    permission = await get_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission_endpoint(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: AsyncSession = Depends(get_db)
):
    permission = await update_permission_service(db, permission_id, permission_data)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission_endpoint(
    permission_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await delete_permission_service(db, permission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Permission not found")
