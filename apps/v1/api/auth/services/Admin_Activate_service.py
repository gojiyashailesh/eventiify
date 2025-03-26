"""This module contains API's specific functionality."""
import uuid
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session # type: ignore


from apps.v1.api.auth import schema
from apps.v1.api.auth.models.methods.method1 import AdminAuthMethod
from apps.v1.api.auth.models.model import Admin

from core.utils import db_method, helper
from core.utils import ValidationMethods
from apps.v1.api.auth.schema import *
#from apps.constant import constant
from core.utils import constant_variable
from core.utils import message_variable

from core.utils.standard_response import StandardResponse
from apps.v1.api.auth import serializer


class AdminAuthActiveService:
    """This class represents the user Activation service"""
    async def active_admin_service(self,db:Session,body:schema.activateAdmin):
        """This Function is used for Activation of User"""
        email = body.email
        #a_status = body.status
        
        admin_object = await AdminAuthMethod(Admin).find_by_email(db,email)
        
        if not admin_object:
            return StandardResponse(
                constant_variable.STATUS_FALSE,
                status.HTTP_404_NOT_FOUND,
                constant_variable.STATUS_NULL,
                message_variable.ERROR_USER_NOT_FOUND
            ).make
            
        admin_object.status = True
        admin_object.deleted_at = None
        time_utils = helper.DateTimeUtils()
        admin_object.updated_at = time_utils.get_time()
        
        await db_method.DataBaseMethod(Admin).save(admin_object,db)
        
        
        if not await db_method.DataBaseMethod(Admin).update(admin_object,db):
            return StandardResponse(
                constant_variable.STATUS_FALSE,
                status.HTTP_400_BAD_REQUEST,
                constant_variable.STATUS_NULL,
                message_variable.ERROR_ADMIN_NOT_ACTIVATE
            ).make
            
        return StandardResponse(
            constant_variable.STATUS_TRUE,
            status.HTTP_200_OK,
            constant_variable.STATUS_NULL,
            message_variable.ERROR_ADMIN_NOT_DEACTIVATE
        ).make
            