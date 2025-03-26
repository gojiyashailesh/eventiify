"""This module contains API's specific functionality."""
import uuid

from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.v1.api.staff.models.methods.method1 import StaffAuthMethod
from apps.v1.api.staff.models.model import Staff
from core.utils import db_method
from core.utils import ValidationMethods
from core.utils import constant_variable as constant
from core.utils import message_variable as message_variable
from core.utils.standard_response import StandardResponse
from datetime import datetime

class StaffAuthService:
    """This class represents the user creation service"""
    async def create_staff_service(self, db: Session, body: dict):
        """This function is used to create user
        Args:
            db (Session): database connection
            body (dict): dictionary to user information data

        Returns:
            response (dict): user object representing the user
        """
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")
        phone_no = body.get("phone_no")
        

        # check Email exists in Db or not
        if await StaffAuthMethod(Staff).find_by_email(db, email):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.AUTH_EMAIL_ALREADY_EXISTS
            ).make

        # For password validation
        if not ValidationMethods().validate_password(password):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                constant.STATUS_NULL, message_variable.INFO_PASSWORD_COMPLEXITY
            ).make

        
        def format_datetime(value):
            if value:
                if isinstance(value, datetime):
                    # Remove timezone info before formatting
                    return value.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
                return str(value)  # Handle cases where value is already a string
            return None
        
        # Create staff object
        staff_object = Staff(
            name=body['name'],
            email=body['email'],
            password=body['password'],
            phone_no=body.get("phone_no"),
            gender=body.get("gender"),
            profile_image=body.get("profile_image",None),
            status=body.get("status", True),
            role_permission_id=body.get("role_permission_id"),
            joining_date=body.get("joining_date"),
            salary=body.get("salary"),
            created_by=body.get("created_by"),
            created_at=format_datetime(body.get("created_at", datetime.utcnow())),
            updated_at=format_datetime(body.get("updated_at")),
            deleted_at=format_datetime(body.get("deleted_at"))
        )
        
        # Store user object in database
        if not await db_method.DataBaseMethod(Staff).save(staff_object, db):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                constant.STATUS_NULL, message_variable.ERROR_USER_NOT_CREATED
            ).make
            
        return StandardResponse(
            True, status.HTTP_200_OK, {
                "name": staff_object.name,
                "email": staff_object.email,
                "password": staff_object.password
            }, message_variable.INFO_USER_CREATED
        ).make

    def get_user_service(self, db):
        """This function returns the user service list."""
        if not (user_object := db_method.BaseMethods(Staff).find_by_uuid(db)):
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                message_variable.ERROR_USER_NOT_FOUND
            )
        # convert the object data into json
        user_data = jsonable_encoder(user_object)

        return StandardResponse(
            True,
            status.HTTP_200_OK,
            user_data,
            message_variable.INFO_USER_RETRIEVED
        )
