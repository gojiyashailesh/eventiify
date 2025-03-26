from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.role.model import Role
from apps.v1.api.role.schemas import RoleCreate, RoleUpdate
from core.db.mixins.save_to_db import save_object


async def find_role_by_id(id: int, db: AsyncSession):
    """Retrieve a role by its ID.

    Args:
        id (int): The role ID to search for.
        db (AsyncSession): The database session.

    Returns:
        Optional[Role]: The role object if found, otherwise None.
    """
    try:
        result = await db.execute(select(Role).where(Role.id == id))
        role = result.scalars().first() 
        return role  
    except Exception as e:
        print(f"Error fetching role by ID {id}: {e}")
        return None
    
async def find_role_by_role(role:str,db:AsyncSession):
    """Retrieve Role By Rolename

    Args:
        role (str): Role Searched by Role Name
        db (AsyncSession): DB Session
    """
    try:
        result = await db.execute(select(Role).where(Role.role==role))
        role = result.scalars().first()
        return role
    except Exception as e:
        print(f"Error Fetching Role with Name{role}:{e}")
        return None


async def create_role(db: AsyncSession, role_data: RoleCreate) -> Optional[Role]:
    """Create a new role in the database.

    Args:
        db (AsyncSession): Database session.
        role_data (RoleCreate): Pydantic model containing role data.

    Returns:
        Optional[Role]: The created role object else none
    """
    try:
        new_role = Role(role=role_data.role)
        return await save_object(db,new_role)
    except SQLAlchemyError as e:
        await db.rollback()  # Rollback on failure
        print(f"Error creating role: {e}")
        return None


async def get_all_roles(db:AsyncSession)->List[Role]:
    """Fetch all role from the databse

    Args:
        db (AsyncSession): db sessions

    Returns:
        List[Role]: return the list of the all the roles
    """
    try:
        result = await db.execute(select(Role))
        return result.scalars().all()  # Fetch all roles properly
    except SQLAlchemyError as e:
        print(f"Error fetching roles: {e}")
        return []  

async def get_role(db: AsyncSession, role_id: int) -> Optional[Role]:
    """get the role 

    Args:
        db (AsyncSession): DB Session
        role_id (int): Role id

    Returns:
        Optional[Role]: Return the Role Or None
    """
    try:
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        print(f"Error fetching role: {e}")
        return None


async def update_role(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
    """update the role

    Args:
        db (AsyncSession): Db Session
        role_id (int): role id to update role
        role_data (RoleUpdate): data to update the role

    Returns:
        Optional[Role]: return the update role
    """
    try:
        role = await get_role(db, role_id)
        if role:
            update_data = role_data.model_dump(exclude_unset=True)  # Use correct method in Pydantic v2
            for key, value in update_data.items():
                setattr(role, key, value)
            await db.commit()
            await db.refresh(role)
            return role
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating role: {e}")
        return None


async def delete_role(db: AsyncSession, role_id: int) -> bool:
    """Remove the Role from the Db

    Args:
        db (AsyncSession): Db session 
        role_id (int): role id which role we need to delete

    Returns:
        bool: if exits and delete return true else false
    """
    try:
        role = await get_role(db, role_id)
        if role:
            await db.delete(role)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting role: {e}")
        return False
