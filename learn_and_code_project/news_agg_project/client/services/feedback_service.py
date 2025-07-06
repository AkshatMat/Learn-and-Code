from client.db.connection import DatabaseConnection
from client.db.modules.article_feedback_manager import ArticleFeedbackManager

class FeedbackService:
    @staticmethod
    def give_feedback(user_id: str, article_id: str, feedback: str):
        with DatabaseConnection.get_cursor() as cursor:
            manager = ArticleFeedbackManager(cursor)
            manager.save_feedback(user_id, article_id, feedback)
