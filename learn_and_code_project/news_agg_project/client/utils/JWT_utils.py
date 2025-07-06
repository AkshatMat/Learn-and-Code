import jwt
import datetime
import os
from dotenv import load_dotenv
from client.utils.exception import JWTError

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

class JWTUtils:
    @staticmethod
    def generate_token(username: str) -> str:
        payload = {
            "username": username,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        
        if not JWT_SECRET or not JWT_ALGORITHM:
            raise JWTError("JWT_SECRET and JWT_ALGORITHM must be configured")
        
        try:
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return token
        except AttributeError as e:
            raise JWTError(f"JWT encoding failed: {str(e)}")
    
    @staticmethod
    def decode_token(token: str) -> dict:
        if not JWT_SECRET or not JWT_ALGORITHM:
            raise JWTError("JWT_SECRET and JWT_ALGORITHM must be configured")
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])            
            return payload
        except jwt.ExpiredSignatureError:
            raise JWTError("Token has expired")
        except jwt.InvalidTokenError:
            raise JWTError("Invalid token")
