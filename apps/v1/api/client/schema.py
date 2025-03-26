from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional
from datetime import datetime
from apps.v1.api.client.models import attribute
from core.utils import helper

class CreateClient(BaseModel):
    """This class is for client schema"""
    name: str
    email: EmailStr
    password: str
    phone_no: str
    gender: attribute.Gender
    profile_image: Optional[bytes] = None
    status: bool
    role_permission_id: int
    last_login_time: Optional[datetime] = None
    created_by: int
    created_at: datetime = helper.DateTimeUtils().get_time()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        """This class schema is for client configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Acme Corp",
                "email": "contact@gmail.com",
                "password": "Secure@123",
                "phone_no": "9876543210",
                "gender":"Male",
                "profile_image": None,
                "status": True,
                "role_permission_id": 1,
                "last_login_time": None,
                "created_by": 1,
            }
        }

# Example validation logic for testing purposes
if __name__ == "__main__":
    try:
        payload = CreateClient(
            name="Acme Corp",
            email="contact@gmail.com",
            password="Secure@123",
            phone_no="9876543210",
            gender="Male",
            status=True,
            role_permission_id=1,
            last_login_time=None,
            created_by=1,
            created_at="2023-11-08T12:00:00Z",
            updated_at="2023-11-09T15:30:00Z"
        )
        print("Validation successful:", payload.json())
    except ValidationError as e:
        print("Validation error:", e.json())


class LoginClient(BaseModel):
    """This class is for client schema"""
    email: EmailStr
    password: str
    status: bool
    role_permission_id: int

    class Config:
        """This class schema is for client configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "client1@gmail.com",
                "password": "Client@123",
                "status": True,
                "role_permission_id": 1
            }
        }
    
class logoutClient(BaseModel):
    """This class is for client logout schema"""
    email: EmailStr
    class Config:
        """This class schema is for client logout configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "client1@gmail.com"
            }
        }   
class resetPasswordClient(BaseModel):
    """This class is for Admin reset password schema"""
    email: EmailStr
    old_password: str
    new_password: str
    confirm_password: str
    updated_at: Optional[datetime] = None
 
    class Config:
        """This class schema is for Admin Reset Password configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "client1@gmail.com",
                "old_password": "Client@123",
                "new_password": "Client@1234",
                "confirm_password": "Client@1234",
            }
        }

class forgotPasswordClient(BaseModel):
    """This class is for Admin Forgot Password Configuration"""
    email : EmailStr
    new_password :str
    confirm_password :str
    updated_at: Optional[datetime] = None
   
    class Config:
        """This is for Forgot Password Configuration"""
        from_attributes = True
        json_schema_extra = {
            "example":{
                "email":"client1@gmail.com",
                "new_password":"Client@1234",
                "confirm_password":"Client@1234"
            }
        }
        
class deactivateClient(BaseModel):
    """This class is for client deactivate schema"""
    email: EmailStr
    class Config:
        """This class schema is for client deactivate configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "client1@gmail.com"
            }
        }

class activateClient(BaseModel):
    """This class is for client activate schema"""
    email: EmailStr
    class Config:
        """This class schema is for client activate configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "client1@gmail.com"
            }
        }