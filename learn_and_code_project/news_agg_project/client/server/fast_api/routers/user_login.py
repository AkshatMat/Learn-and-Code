from fastapi import APIRouter, HTTPException
from client.server.fast_api.schemas.schemas import LogInParams
from client.services.user_login_service import UserLogInService

router = APIRouter()

login_service = UserLogInService()

@router.post("/")
def login_user(params: LogInParams):
    try:
        if not params.username or not params.password:
            raise HTTPException(status_code=400, detail="All fields (username, password) are required and cannot be empty")
        
        result = login_service.login(params)
        
        if 'error' in result:
            raise HTTPException(status_code=401, detail=result['error'])
        
        return {"message": "User login successful", "token": result["token"], "user_id": result["user_id"]}

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

