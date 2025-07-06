import uuid
import bcrypt
from client.utils.logger import logger
from client.utils.exception import DatabaseError

class ArticleFeedbackManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def save_feedback(self, user_id: str, article_id: str, feedback: str):
        query = """
            INSERT INTO article_feedback_table (user_id, article_id, feedback)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, article_id)
            DO UPDATE SET feedback = EXCLUDED.feedback;
        """
        self.cursor.execute(query, (user_id, article_id, feedback))

    def get_feedback_by_user(self, user_id: str):
        query = """
            SELECT article_id, feedback, created_at
            FROM article_feedback_table
            WHERE user_id = %s;
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
