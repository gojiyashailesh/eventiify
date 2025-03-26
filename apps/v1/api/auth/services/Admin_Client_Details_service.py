"""This module contains API's specific functionality."""
import uuid
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session # type: ignore


from apps.v1.api.auth import schema
from apps.v1.api.auth.models.methods.method1 import AdminAuthMethod
from apps.v1.api.auth.models.model import Admin

from apps.v1.api.client.models.model import Client
from core.utils import db_method, helper
from core.utils import ValidationMethods
from apps.v1.api.auth.schema import *
#from apps.constant import constant
from core.utils import constant_variable
from core.utils import message_variable

from core.utils.standard_response import StandardResponse
from apps.v1.api.auth import serializer


class clientDetailService:
    """This class is for fetching all Client Details"""
    
    async def get_all_client_details_service(self, db: Session):
        """This function retrieves all client details from the database"""
        # Fetching all client records from the database
        client_objects = await db_method.DataBaseMethod(Client).find_all(db)
        
        if not client_objects:
            return StandardResponse(
                constant_variable.STATUS_FALSE,
                status.HTTP_404_NOT_FOUND,
                constant_variable.STATUS_NULL,
                message_variable.ERROR_NO_CLIENTS_FOUND
            ).make
        
        # Mapping the fetched data to schema ClientDetails
        client_details_list = [
            schema.ClientDetails(
                name=client.name,
                email=client.email,
                phone_no=client.phone_no,
                profile_image=client.profile_image,
                status=client.status,
                role_permission_id=client.role_permission_id,
                created_by=client.created_by,
                created_at=client.created_at,
                updated_at=client.updated_at,
                deleted_at=client.deleted_at
            )
            for client in client_objects
        ]
        
        return client_details_list