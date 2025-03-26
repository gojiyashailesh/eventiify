from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.v1.api.auth.services.service import AdminAuthService
from apps.v1.api.auth import schema
from core.utils import message_variable
from core.utils.standard_response import StandardResponse
from config import db_config
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

## Load API's
router = APIRouter()
getdb = db_config.get_db

## Define version 1 API's here
class AdminCrudApi():
    """This class is for client CRUD operation with version 1 API's"""
    @router.post("/create/admin", response_model=schema.CreateAdmin)
    async def create_admin(body: schema.CreateAdmin, db: Session = Depends(getdb)):
        try:
            # Decode the Base64-encoded image if it exists
            if body.profile_image:
                try:
                    # Remove the prefix if it's a data URL (e.g., data:image/png;base64,...)
                    if body.profile_image.startswith("data:image"):
                        body.profile_image = body.profile_image.split(",")[1]

                    # Decode the Base64-encoded image
                    body.profile_image = base64.b64decode(body.profile_image)
                except Exception as e:
                    logger.error(f"Invalid image format: {e}")
                    raise HTTPException(status_code=400, detail="Invalid image format")

            # Convert body to dict for compatibility with your service
            body_data = body.dict()  # Use .dict() instead of .model_dump()
            print(f"Body Data is : {body_data}")
            # Call the service layer to create client
            response = await AdminAuthService().create_admin_service(db, body_data)
            print(f"Res: {response}")
            return response
        
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_INTERNAL_SERVER)
        

    @router.post("/login/admin", response_model=schema.loginAdmin,status_code=status.HTTP_200_OK)
    async def login_admin(body: schema.loginAdmin, db: Session = Depends(getdb)):
        """Login API for admin"""
        try:
            response = await AdminAuthService().login_admin_service(db, body)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_LOGIN_FAILED)
    
