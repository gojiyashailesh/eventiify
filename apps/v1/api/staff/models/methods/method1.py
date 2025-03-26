"""This module contains database operations methods."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Use select() for async queries
from sqlalchemy.exc import NoResultFound
from core.utils import message_variable

class StaffAuthMethod:
    """This class defines methods to authenticate users."""

    def __init__(self, model) -> None:
        self.model = model

    async def find_by_email(self, db: AsyncSession, email: str):
        """This function will return the email object asynchronously."""
        try:
            result = await db.execute(select(self.model).filter(self.model.email == email.strip()))
            staff_data = result.scalars().first()

            if staff_data:
                print(f"Email {email} already exists in the database.")
                return staff_data  # Return found data
            else:
                print(f"Email {email} not found in the database.")
                return None        # Return None if not found

        except Exception as e:
            print(f"Exception in find_by_email: {e}")
            return None  # Return None on exception to prevent breaking logic


    async def find_by_name(self, db: AsyncSession, name: str):
        """This function will return the name object asynchronously."""
        try:
            result = await db.execute(select(self.model).filter(self.model.name == name))
            return result.scalars().first()
        except NoResultFound:
            return None
