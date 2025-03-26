"""This module contains API's specific functionality."""
import uuid

from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session # type: ignore

from datetime import datetime
from apps.v1.api.auth.models.methods.method1 import AdminAuthMethod
from apps.v1.api.auth.models.model import Admin
from apps.v1.api.auth.schema import loginAdmin
from core.utils import db_method
from core.utils import ValidationMethods

#from apps.constant import constant
from core.utils import constant_variable as constant
from core.utils import message_variable
from core.utils.message_variable import ERROR_MSG, INFO_MSG as msg_var
from core.utils.standard_response import StandardResponse

class AdminAuthService:
    """This class represents the user creation service"""
    async def create_admin_service(self, db: Session, body: dict):
        """This function is used to create client"""

        print("1")
        email = body["email"]
        print("2")
        # Check if email already exists
        if await AdminAuthMethod(Admin).find_by_email(db, email):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.AUTH_EMAIL_ALREADY_EXISTS
            ).make
        print("3")
        # Validate password format
        if not ValidationMethods().validate_password(body["password"]):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.INFO_PASSWORD_COMPLEXITY
            ).make
        print("4")
        def format_datetime(value):
            if value:
                if isinstance(value, datetime):
                    # Remove timezone info before formatting
                    return value.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
                return str(value)  # Handle cases where value is already a string
            return None
        # Create admin object
        admin_object = Admin(
            name=body['name'],
            email=body['email'],
            password=body['password'],
            phone_no=body.get("phone_no"),
            gender = body.get("gender"),
            profile_image=body.get("profile_image",None),
            status=body.get("status", True),
            role_permission_id=body.get("role_permission_id"),
            last_login_time=format_datetime(body.get("last_login_time")),
            created_at=format_datetime(body.get("created_at", datetime.utcnow())),
            updated_at=format_datetime(body.get("updated_at")),
            deleted_at=format_datetime(body.get("deleted_at"))
        )
        print(f"Admin Object in service :{admin_object.__dict__}")
        # Store user object in database
        if not await db_method.DataBaseMethod(Admin).save(admin_object, db):   
            print(f"Inside the if condition {admin_object}")
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.ERROR_USER_NOT_CREATED
            ).make
        print("5")
        
        return StandardResponse(
            True, status.HTTP_200_OK, {
                "name": admin_object.name,
                "email": admin_object.email,
                "password": admin_object.password
            }, message_variable.INFO_USER_CREATED
        ).make


    def get_admin_service(self, db):
        """This function returns the user service list."""
        """if not (client_object := db_method.DataBaseMethod(Client).find_by_uuid(db)):
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                message_variable.ERROR_USER_NOT_FOUND
            )"""
        # convert the object data into json
        user_data = jsonable_encoder(admin_object)

        return StandardResponse(
            True,
            status.HTTP_200_OK,
            user_data,
            message_variable.INFO_USER_RETRIEVED
        )
        
    async def login_admin_service(self, db: Session, body: loginAdmin):
        email = body.email
        password = body.password  

        admin_object = await AdminAuthMethod(Admin).find_by_email(db, email)
        if not admin_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_EMAIL_NOT_EXISTS
            ).make

        if password != admin_object.password:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_INVALID_PASSWORD
            ).make

        admin_object.last_login_time = datetime.utcnow()
        db.add(admin_object)
        await db.commit()
        await db.refresh(admin_object)  # Ensures the updated data is available

        return StandardResponse(
            True, status.HTTP_200_OK, {
                "name": admin_object.name,
                "email": admin_object.email,
                "password": admin_object.password
            }, message_variable.SUCCESS_LOGIN
        ).make
