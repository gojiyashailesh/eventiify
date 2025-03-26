from pydantic import BaseModel, EmailStr, ValidationError
from typing import Literal, Optional
from datetime import datetime,date

class CreateStaff(BaseModel):
    """This class is for client schema"""
    name: str
    email: EmailStr
    password: str
    phone_no: str
    gender: Literal['MALE', 'FEMALE']
    profile_image: Optional[bytes] = None
    status: bool
    role_permission_id: int
    created_by: int
    joining_date: date
    salary:int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        """This class schema is for staff configuration"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Acme Corp",
                "email": "contact@gmail.com",
                "password": "Secure@123",
                "phone_no": "9876543210",
                "gender":"MALE",
                "profile_image": None,
                "status": True,
                "role_permission_id": 1,
                "created_by": 7,
                "joining_date":"2023-11-08",
                "salary":50000,
                "created_at": "2023-11-08T12:00:00Z",
                "updated_at": "2023-11-09T15:30:00Z",
                "deleted_at": None
            }
        }

# Example validation logic for testing purposes
if __name__ == "__main__":
    try:
        payload = CreateStaff(
            name="Acme Corp",
            email="contact@gmail.com",
            password="Secure@123",
            phone_no="9876543210",
            gender="MALE",
            status=True,
            role_permission_id=1,
            joining_date="2023-11-08",
            salary=50000,
            created_by=1,
            created_at="2023-11-08T12:00:00Z",
            updated_at="2023-11-09T15:30:00Z"
        )
        print("Validation successful:", payload.json())
    except ValidationError as e:
        print("Validation error:", e.json())
