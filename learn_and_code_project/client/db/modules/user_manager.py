import uuid
from client.utils.logger import logger
from client.utils.exception import DatabaseError

class UserManager:
    def __init__(self, cursor):
        self.cursor = cursor
        
    def insert_user(self, username: str, email: str, hashed_password: str, role: str):
        try:
            user_uuid = str(uuid.uuid4())
            
            insert_script = '''
                INSERT INTO user_table (uuid, username, email, password, role)
                VALUES (%s,%s ,%s, %s, %s);
            '''
            self.cursor.execute(insert_script, (user_uuid, username, email, hashed_password, role))
            logger.info("User added successfully.")
        except Exception as e:
            logger.error(f"Error inserting user: {e}")
            raise DatabaseError("Error inserting user")

    def fetch_user(self, username: str):
        try:
            select_query = """
                SELECT uuid, username, password, role
                FROM user_table
                WHERE LOWER(username) = LOWER(%s);
            """
            self.cursor.execute(select_query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            raise DatabaseError("Error fetching user")