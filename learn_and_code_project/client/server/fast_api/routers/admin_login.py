from fastapi import APIRouter, HTTPException
from client.server.fast_api.schemas.schemas import LogInParams
from client.services.admin_login_service import AdminLogInService

router = APIRouter()

login_service = AdminLogInService()

@router.post("/")
def login_admin(params: LogInParams):
    try:
        if not params.username or not params.password:
            raise HTTPException(status_code=400, detail="All fields (username, password) are required and cannot be empty")
        
        result = login_service.login(params)
        
        if 'error' in result:
            raise HTTPException(status_code=401, detail=result['error'])
        
        return {"message": "Admin login successful", "token": result["token"]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))