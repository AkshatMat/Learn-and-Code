import uuid
import bcrypt
from client.utils.logger import logger
from client.utils.exception import DatabaseError

class AdminManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_admin(self, username: str):
        try:
            query = """
                SELECT uuid, username, password, role
                FROM user_table
                WHERE LOWER(username) = LOWER(%s) AND role = 'Admin';
            """
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching admin: {e}")
            raise DatabaseError("Failed to fetch admin")

    def insert_admin(self, username: str, plain_password: str):
        try:
            hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_id = str(uuid.uuid4())

            insert_query = """
                INSERT INTO user_table (uuid, username, password, role)
                VALUES (%s, %s, %s, %s);
            """
            self.cursor.execute(insert_query, (admin_id, username, hashed_password, 'Admin'))
            logger.info(f"Admin user '{username}' inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting admin: {e}")
            raise DatabaseError("Failed to insert admin")