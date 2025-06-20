from client.db.connection import DatabaseConnection
from client.utils.password_hasher import hash_password
from client.db.modules.user_manager import UserManager
from client.server.fast_api.schemas.schemas import SignUpParams
from client.utils.logger import logger

class SignupService:
    def signup(self, params: SignUpParams):
        try:
            hashed_password = hash_password(params.password)
            
            with DatabaseConnection.get_cursor() as cursor:
                user_manager = UserManager(cursor)
                user_manager.insert_user(params.username, params.email, hashed_password, params.role)
                
        except Exception as e:
            logger.error(f"Error during signup: {e}")
            raise Exception("An error occurred during signup")