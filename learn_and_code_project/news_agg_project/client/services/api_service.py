from client.db.connection import DatabaseConnection
from client.db.modules.api_manager import APIManager
from client.utils.exception import ServiceError

class APIService:
    @staticmethod
    def get_all_apis():
        try:
            with DatabaseConnection.get_cursor() as cursor:
                return APIManager(cursor).get_all_apis()
        except Exception as e:
            raise ServiceError(f"Failed to get API details: {str(e)}")

    @staticmethod
    def get_api_by_name(api_name: str):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                return APIManager(cursor).get_api_by_name(api_name)
        except Exception as e:
            raise ServiceError(f"Failed to get API by name: {str(e)}")

    @staticmethod
    def upsert_api(api_url: str, status: str, api_key: str, name: str):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                APIManager(cursor).upsert_api(api_url, status, api_key, name)
        except Exception as e:
            raise ServiceError(f"Failed to upsert API: {str(e)}")

    @staticmethod
    def delete_api(api_url: str):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                return APIManager(cursor).delete_api(api_url)
        except Exception as e:
            raise ServiceError(f"Failed to delete API: {str(e)}")

    @staticmethod
    def update_api_status(api_name: str, status: str):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                return APIManager(cursor).update_api_status(api_name, status)
        except Exception as e:
            raise ServiceError(f"Failed to update API status: {str(e)}") 