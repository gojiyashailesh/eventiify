from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional,Literal
from datetime import datetime

class CreateAdmin(BaseModel):
    """This class is for client schema"""
    name: str
    email: EmailStr
    password: str
    phone_no: str
    gender: Literal['MALE', 'FEMALE'] 
    profile_image: Optional[bytes] = None
    status: bool
    last_login_time: Optional[datetime] = None
    role_permission_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        """This class schema is for client configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Admin",
                "email": "admin@gmail.com",
                "password": "admin@123",
                "phone_no": "9876543210",
                "gender":"FEMALE",
                "profile_image": None,
                "status": True,
                "last_login_time": "2024-10-01T09:00:00",
                "role_permission_id": 1,
                "created_at": "2024-10-01T09:00:00",
                "updated_at": "2024-10-01T09:30:00",
                "deleted_at": None
            }
        }

class loginAdmin(BaseModel):
    """This class is for Admin login schema"""
    email: EmailStr
    password: str
    last_login_time: Optional[datetime] = None
    status: bool
    role_permission_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        """This class schema is for Admin configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin@123",
                "last_login_time": "2024-10-01T09:00:00",
                "status": True,
                "role_permission_id": 1,
                "created_at": "2024-10-01T09:00:00",
                "updated_at": "2024-10-01T09:30:00",
                "deleted_at": None
            }
        }
        

# Example validation logic for testing purposes
"""
if __name__ == "__main__":
    try:
        payload = CreateAdmin(
            name="Acme Corp",
            email="contact@gmail.com",
            password="Secure@123",
            phone_no="9876543210",
            status=True,
            role_permission_id=1,
            created_at="2023-11-08T12:00:00Z",
            updated_at="2023-11-09T15:30:00Z"
        )
        print("Validation successful:", payload.json())
    except ValidationError as e:
        print("Validation error:", e.json())
"""