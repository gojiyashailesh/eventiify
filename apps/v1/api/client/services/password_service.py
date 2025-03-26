"""This module contains API's specific functionality."""
import uuid

from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from datetime import datetime,timedelta
from apps.v1.api.client.models.methods.method1 import ClientAuthMethod
from apps.v1.api.client.models.model import Client
from core.utils import db_method
from core.utils import ValidationMethods
#from apps.constant import constant
from core.utils import constant_variable as constant
from core.utils import message_variable
from core.utils.message_variable import ERROR_MSG, INFO_MSG as msg_var
from core.utils.standard_response import StandardResponse

class ClientResetOrForgotPassword:
    async def reset_password_service(self, db: Session, body: dict):
        email = body["email"]
        old_password = body["old_password"]
        new_password = body["new_password"]
        confirm_password = body["confirm_password"]
       
        # Check if admin already exists
        client_object = await ClientAuthMethod(Client).find_by_email(db, email)
        if not client_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_PASSWORD_RESET_FAILED
            ).make
 
        # Check Old Password
        if old_password != client_object.password:
            print(f"Old Password is {old_password} and Admin Password is {client_object.password}")
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.INVALID_INPUT
            ).make
           
        # Check New Password and Confirm Password
        if new_password != confirm_password:
            print(f"New Password is {new_password} and Confirm Password is {confirm_password}")
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.AUTH_PASSWORD_MISMATCH
            ).make
        
        if not ValidationMethods().validate_password(new_password):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,{
                    "Password Error": message_variable.INFO_PASSWORD_COMPLEXITY
                },
                message_variable.INFO_PASSWORD_COMPLEXITY
            ).make
   
        # Update Password
        client_object.password = new_password
        client_object.updated_at = datetime.utcnow() + timedelta(hours=5, minutes=30)
        
        if not await db_method.DataBaseMethod(Client).save(client_object, db):   
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.ERROR_PASSWORD_RESET
            )

        """
        db.add(client_object)
        await db.commit()
        await db.refresh(client_object)
       """
       
        return StandardResponse(
            True,status.HTTP_200_OK,None,
            message_variable.AUTH_PASSWORD_RESET_SUCCESS
        ).make        


    async def forgot_password_service(self, db: Session, body: dict):
        email = body["email"]
        new_password = body["new_password"]
        confirm_password = body["confirm_password"]
       
        # Check if admin already exists
        client_object = await ClientAuthMethod(Client).find_by_email(db, email)
        if not client_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_EMAIL_NOT_EXISTS
            ).make
           
        if new_password != confirm_password:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.AUTH_PASSWORD_MISMATCH
            ).make
       
        # Validate password format
        if not ValidationMethods().validate_password(new_password):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,None,
                message_variable.INFO_PASSWORD_COMPLEXITY
            ).make
       
        # Update Password
        client_object.password = new_password
        client_object.updated_at = datetime.utcnow() + timedelta(hours=5, minutes=30)
        db.add(client_object)
        await db.commit()
        await db.refresh(client_object)
       
        return StandardResponse(
            True,status.HTTP_200_OK,None,
            message_variable.AUTH_PASSWORD_RESET_SUCCESS
        ).make