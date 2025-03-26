from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """Pydantic model for Role"""
    role: str = Field(description="Name of the Role Required")

    class Config:
        """Configuration Class"""
        from_attributes = True  # Enable ORM mode in Pydantic v2
        json_schema_extra = {
            "example": {
                "role": "Admin"
            }
        }

    def json_schema(self):
        """Returns the JSON schema of the model."""
        return self.model_json_schema()



class RoleCreate(RoleBase):
    """Defined the Schema for Val

    Args:
        RoleBase (basemodel): RoleBase
    """
    pass

class RoleUpdate(RoleBase):
    """Defined the schema for val"""
    pass

class RoleResponse(RoleBase):
    """Defined the schemas for the validation """
    id: int
    
    class Config:
        """added the schema show val"""
        orm_mode = True