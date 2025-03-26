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
from core.utils import helper

class Deactivate_Client_account:
    async def deactivate_client_account(self, db: Session, body: dict):
        email = body["email"]
        client_object = await ClientAuthMethod(Client).find_by_email(db, email)
        if not client_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_EMAIL_NOT_EXISTS
            ).make
        client_object.status = False
        client_object.updated_at = helper.DateTimeUtils().get_time()
        
        if not await db_method.DataBaseMethod(Client).save(client_object, db):   
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.ERROR_USER_UPDATE
            )
        
        return StandardResponse(
            True, status.HTTP_200_OK, None,
            message_variable.SUCCESS_USER_UPDATE
        ).make
        
class Activate_Client_account:
    async def activate_client_account(self, db: Session, body: dict):
        email = body["email"]
        client_object = await ClientAuthMethod(Client).find_by_email(db, email)
        if not client_object:
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST, None,
                message_variable.AUTH_EMAIL_NOT_EXISTS
            ).make
        client_object.status = True
        client_object.updated_at = helper.DateTimeUtils().get_time()
        
        if not await db_method.DataBaseMethod(Client).save(client_object, db):   
            return StandardResponse(
                False, status.HTTP_400_BAD_REQUEST,
                message_variable.ERROR_USER_UPDATE
            )
        
        return StandardResponse(
            True, status.HTTP_200_OK, None,
            message_variable.SUCCESS_USER_UPDATE
        ).make