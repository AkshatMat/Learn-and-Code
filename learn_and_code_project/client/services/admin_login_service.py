from client.server.fast_api.schemas.schemas import LogInParams
from client.utils.JWT_utils import JWTUtils
from client.utils.logger import logger
from client.db.modules.admin_manager import AdminManager
from client.utils.password_verification import PasswordUtils
from client.db.connection import DatabaseConnection

class AdminLogInService:
    def login(self, params: LogInParams):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                user = AdminManager(cursor).fetch_admin(params.username)
                if not user:
                    return {"error": "Invalid username or password"}

                stored_password = user["password"]

                if not PasswordUtils.verify_password(params.password, stored_password):
                    return {"error": "Invalid username or password"}

                token = JWTUtils().generate_token(params.username)
                return {"token": token}

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {"error": "An error occurred during login"}
