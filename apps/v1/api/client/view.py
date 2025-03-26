from fastapi import APIRouter, Depends, HTTPException, status,Request,Response
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.orm import Session
from apps.v1.api.client.services.service import ClientAuthService
from apps.v1.api.client.services.password_service import ClientResetOrForgotPassword
from apps.v1.api.client.services.activation_service import Activate_Client_account,Deactivate_Client_account
from apps.v1.api.client import schema
from core.utils import message_variable
from core.utils.standard_response import StandardResponse
from config import db_config
import logging
import base64
from core.session import SessionService,EnrytionDecrytionUtils


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

## Load API's
router = APIRouter()
getdb = db_config.get_db

## Define version 1 API's here
class ClientCrudApi():
    """This class is for client CRUD operation with version 1 API's"""
    @router.post("/Newclient", response_model=schema.CreateClient)
    async def create_client(body: schema.CreateClient, db: Session = Depends(getdb)):
        try:
            if body.profile_image:
                body.profile_image = await ClientAuthService().decode_image(body.profile_image)
            """
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
            """
           
            # Convert body to dict for compatibility with your service
            body_data = body.dict()  # Use .dict() instead of .model_dump()
            print(f"Body Data is : {body_data}")
            # Call the service layer to create client
            response = await ClientAuthService().create_client_service(db, body_data)
            print(f"Res: {response}")
            return response
        
        except Exception as e:
            raise HTTPException(status_code=500,detail=message_variable.ERROR_USER_NOT_CREATED)


class ClientAuthApi():
    """This class is for client authentication with version 1 API's"""
    @router.post("/client/login", response_model=schema.LoginClient)
    async def login_client(request: Request, response: Response,body: schema.LoginClient, db: Session = Depends(getdb)):
        """Login API for client"""
        body_data = body.dict()
        try:
            response = await ClientAuthService().login_client_service(db, body_data)
            if response:
                session_service = SessionService()
                session_cookie = session_service.generate_session_functionality(
                    request=request,
                    email=body_data.get("email"),
                    role_permission_id=body_data.get("role_permission_id"),
                    role="staff")
                
                response.set_cookie(**session_cookie)
                session_key = session_cookie.get("value")
                
                decoded_session_key = session_service.signer.unsign(session_key, max_age=3600)
                #print(f"\nDecoded Session Key: {decoded_session_key}")  # Debugging

                # Get session data using the decoded session key
                session_data = session_service.get_session_context(decoded_session_key) 
                if session_data:
                    decrypted_data = EnrytionDecrytionUtils().decrypt_data(session_data)
                    #print(f"Decrypted session data: {decrypted_data}")
                print("session key is :",session_key)
                print("\n\nSession Data:", decrypted_data)  # Debugging
                
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.AUTH_USER_NOT_REGISTERED)
    
    """        
    @router.post("/client/logout")
    async def logout_client(request: Request, response: Response,body:schema.logoutClient,db: Session = Depends(getdb)):
        #Logout API for client
        session_service = SessionService()
        email = body.email
        session_key = request.cookies.get("session")

        if session_key:
            try:
                # Log the session key and check its format
                print(f"Session Key from Cookie: {session_key}")
                
                # Unsigned session key (decode the session key to retrieve the original session ID)
                decoded_session_key = session_service.signer.unsign(session_key, max_age=3600)  # Adjust max_age if needed
                print(f"Decoded Session Key: {decoded_session_key}")
                
                session_data = session_service.get_session_context(decoded_session_key)
                print(f"Session Data: {session_data}")
                
                if session_data:
                    # Decrypt the session data to extract email and validate the session
                    decrypted_data = EnrytionDecrytionUtils().decrypt_data(session_data)
                    print(f"Decrypted Session Data: {decrypted_data}")
                    
                    # Ensure the email in session matches the one provided in the logout request
                    if decrypted_data.get("email") == email:
                        # Invalidate the session from the session store (e.g., Redis)
                        session_service.invalidate_session(decoded_session_key)
                        
                        # Delete session cookie
                        response.delete_cookie("session")

                        return StandardResponse(
                            success=True,
                            status_code=status.HTTP_200_OK,
                            data=None,  # No additional data on logout
                            message=f"Logged out successfully for {email}."
                        ).make()
                    else:
                        raise HTTPException(status_code=400, detail="Session email mismatch.")
                else:
                    raise HTTPException(status_code=400, detail="Invalid session.")
            except Exception as e:
                print(f"Error during unsigning session: {e}")
                raise HTTPException(status_code=400, detail="Invalid session key.")
        else:
            raise HTTPException(status_code=400, detail="Session not found.")
    """
        
    @router.post("/client/reset-password", response_model=schema.resetPasswordClient)
    async def reset_password(body: schema.resetPasswordClient, db: Session = Depends(getdb)):
        """Reset password API for client"""
        body_data = body.dict()
        try:
            response = await ClientResetOrForgotPassword().reset_password_service(db, body_data)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_PASSWORD_RESET)
        
    @router.post("/client/forgot-password", response_model=schema.forgotPasswordClient)
    async def forgot_password(body: schema.forgotPasswordClient, db: Session = Depends(getdb)):
        """Forgot password API for client"""
        body_data = body.dict()
        try:
            response = await ClientResetOrForgotPassword().forgot_password_service(db, body_data)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_PASSWORD_RESET)
        
    @router.post("/client/activate-account", response_model=schema.activateClient)
    async def activate_account(body: schema.activateClient, db: Session = Depends(getdb)):
        """Activate account API for client"""
        body_data = body.dict()
        try:
            response = await Activate_Client_account().activate_client_account(db, body_data)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_USER_UPDATE)
        
    @router.post("/client/deactivate-account", response_model=schema.deactivateClient)
    async def deactivate_account(body: schema.deactivateClient, db: Session = Depends(getdb)):
        """Deactivate account API for client"""
        body_data = body.dict()
        try:
            response = await Deactivate_Client_account().deactivate_client_account(db, body_data)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500,detail=message_variable.ERROR_USER_UPDATE)