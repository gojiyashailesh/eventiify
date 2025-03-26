"""This module contains database operations methods."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Use select() for async queries
from sqlalchemy.exc import NoResultFound
from core.utils import message_variable

class AdminAuthMethod:
    """This class defines methods to authenticate users."""

    def __init__(self, model) -> None:
        self.model = model

    async def find_by_email(self, db: AsyncSession, email: str):
        """This function will return the email object asynchronously."""
        try:
            result = await db.execute(select(self.model).filter(self.model.email == email))
            print(f"result is {result}")
            return result.scalars().first()
            
        except NoResultFound:
            return None

    async def find_by_name(self, db: AsyncSession, name: str):
        """This function will return the name object asynchronously."""
        try:
            result = await db.execute(select(self.model).filter(self.model.name == name))
            return result.scalars().first()
        except NoResultFound:
            return None
