from datetime import datetime
from client.utils.logger import logger
from client.utils.exception import ManagerError

class APIManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_apis(self):
        """Get all API details with name and status"""
        try:
            query = """
                SELECT name, status, api_url, last_accessed
                FROM api_table
                ORDER BY name
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                if isinstance(row, dict):
                    result.append(row)
                else:
                    result.append({
                        'name': row[0],
                        'status': row[1], 
                        'api_url': row[2],
                        'last_accessed': row[3]
                    })
            return result
        except Exception as e:
            logger.error(f"Error fetching API details: {e}")
            raise ManagerError(f"Failed to fetch API details: {str(e)}")

    def get_api_by_name(self, api_name: str):
        try:
            query = """
                SELECT api_url, status, api_key, name, last_accessed
                FROM api_table
                WHERE name = %s
            """
            self.cursor.execute(query, (api_name,))
            row = self.cursor.fetchone()
            
            if not row:
                return None
                
            if isinstance(row, dict):
                return row
            else:
                return {
                    'api_url': row[0],
                    'status': row[1],
                    'api_key': row[2],
                    'name': row[3],
                    'last_accessed': row[4]
                }
        except Exception as e:
            logger.error(f"Error fetching API by name: {e}")
            raise ManagerError(f"Failed to fetch API by name: {str(e)}")

    def upsert_api(self, api_url: str, status: str, api_key: str, name: str):
        try:
            query = """
                INSERT INTO api_table (api_url, status, api_key, name, last_accessed)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (api_url) DO UPDATE SET
                    status = EXCLUDED.status,
                    api_key = EXCLUDED.api_key,
                    name = EXCLUDED.name
            """
            self.cursor.execute(query, (api_url, status, api_key, name))
            logger.info(f"API '{name}' upserted successfully")
        except Exception as e:
            logger.error(f"Error upserting API: {e}")
            raise ManagerError(f"Failed to upsert API: {str(e)}")

    def delete_api(self, api_url: str):
        try:
            query = "DELETE FROM api_table WHERE api_url = %s"
            self.cursor.execute(query, (api_url,))
            if self.cursor.rowcount > 0:
                logger.info(f"API with URL '{api_url}' deleted successfully")
                return True
            else:
                logger.warning(f"API with URL '{api_url}' not found")
                return False
        except Exception as e:
            logger.error(f"Error deleting API: {e}")
            raise ManagerError(f"Failed to delete API: {str(e)}")

    def update_api_status(self, api_name: str, status: str):
        try:
            query = """
                UPDATE api_table
                SET status = %s
                WHERE name = %s
            """
            self.cursor.execute(query, (status, api_name))
            if self.cursor.rowcount > 0:
                logger.info(f"API '{api_name}' status updated to '{status}'")
                return True
            else:
                logger.warning(f"API '{api_name}' not found")
                return False
        except Exception as e:
            logger.error(f"Error updating API status: {e}")
            raise ManagerError(f"Failed to update API status: {str(e)}") 