"""This module contains API's specific functionality."""
import uuid

from fastapi import status,HTTPException
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
import base64
import logging
from apps.v1.api.client import serializer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class ClientAuthService:
    """This class represents the user creation service"""
    print("1")
    
    async def decode_image(self, profile_image: str) -> bytes:
        if profile_image:
            try:
                # Remove the prefix if it's a data URL (e.g., data:image/png;base64,...)
                if profile_image.startswith("data:image"):
                    profile_image = profile_image.split(",")[1]

                # Decode the Base64-encoded image
                return base64.b64decode(profile_image)
            except Exception as e:
                logger.error(f"Invalid image format: {e}")
                raise HTTPException(status_code=400, detail="Invalid image format")
        return None     
    
    async def create_client_service(self, db: Session, body: dict):
        """This function is used to create client"""

        email = body["email"]
        print("2")
        print(f"Email is :{email}")
        
      
        # Check if email already exists
        if await ClientAuthMethod(Client).find_by_email(db, email):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.AUTH_EMAIL_ALREADY_EXISTS
            ).make
        print("3")
        # Validate password format
        if not ValidationMethods().validate_password(body["password"]):
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.INFO_PASSWORD_COMPLEXITY
            ).make

         # Decode profile image
        if body.get("profile_image"):
            body["profile_image"] = await self.decode_image(body["profile_image"])

        def format_datetime(value):
            if value:
                if isinstance(value, datetime):
                    # Remove timezone info before formatting
                    return value.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
                return str(value)  # Handle cases where value is already a string
            return None
        print("4")
        # Create client object
        """
        client_object = Client(
            name=body['name'],
            email=body['email'],
            password=body['password'],
            phone_no=body.get("phone_no"),
            profile_image=body.get("profile_image",None),
            status=body.get("status", True),
            role_permission_id=body.get("role_permission_id"),
            created_by=body.get("created_by"),
            created_at=format_datetime(body.get("created_at", datetime.utcnow())),
            updated_at=format_datetime(body.get("updated_at")),
            deleted_at=format_datetime(body.get("deleted_at"))
        )
        """
        client_object = Client(**body)
        print(f"Cleint Object is :{client_object}")
        # Store user object in database
        if not await db_method.DataBaseMethod(Client).save(client_object, db):   
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.ERROR_USER_NOT_CREATED
            )

        return StandardResponse(
            True, status.HTTP_200_OK,
            serializer.serializer_client(client_object),
            message_variable.INFO_USER_CREATED
        ).make


    async def login_client_service(self, db: Session, body: dict):        
        """This API is used to login client"""
        
        email = body["email"]
        password = body["password"]
        c_status = body["status"]
        
        client_object = await ClientAuthMethod(Client).find_by_email(db, body["email"])
        if not client_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.ERROR_LOGIN_FAILED
            ).make
        #print("client found")
        #print("password is : ",password)
        #print("client_object.password is : ",client_object.password)
        if password != client_object.password:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,{
                    "password":password,
                },
                message_variable.ERROR_PASSWORD_MISMATCH
            ).make 
        #print("password match")
        if c_status != client_object.status:
            return StandardResponse(
                False, 
                status.HTTP_400_BAD_REQUEST,
                message_variable.AUTH_ACCOUNT_DISABLED,  # Message should come before additional data
                {"Account is Active": client_object.status}  # Corrected position for the dictionary
            ).make

        #print("status true")
        return StandardResponse(
            True, status.HTTP_200_OK, 
            serializer.serializer_client(client_object),   
            message_variable.SUCCESS_LOGIN
        ).make
        
    async def logout_client_service(self,body: dict):
        """This function is used to logout client"""
        
        email = body["email"]
        
        return StandardResponse(
            True, status.HTTP_200_OK, None, message_variable.SUCCESS_LOGOUT
        ).make
    
    """
    def get_client_service(self, db):
        This function returns the user service list.
        if not (client_object := db_method.DataBaseMethod(Client).find_by_uuid(db)):
            return StandardResponse(
                False,
                status.HTTP_400_BAD_REQUEST,
                None,
                message_variable.ERROR_USER_NOT_FOUND
            )
        # convert the object data into json
        user_data = jsonable_encoder(client_object)

        return StandardResponse(
            True,
            status.HTTP_200_OK,
            user_data,
            message_variable.INFO_USER_RETRIEVED
        )
        """
