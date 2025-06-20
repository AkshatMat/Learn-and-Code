from fastapi import APIRouter, HTTPException
from client.server.fast_api.schemas.schemas import SignUpParams
from client.services.signup_service import SignupService

router = APIRouter()

signup_service = SignupService()

@router.post("/")
def signup_user(params: SignUpParams):
    try:
        if not params.username or not params.email or not params.password:
            raise HTTPException(status_code=400, detail="All fields (username, email, password) are required and cannot be empty")

        signup_service.signup(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User registered successfully"}
