from client.db.connection import DatabaseConnection
from client.db.modules.saved_article_manager import SavedArticleManager

class UserService:
    @staticmethod
    def save_article(user_id: str, article_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            return SavedArticleManager(cursor).save_article(user_id, article_id)

    @staticmethod
    def get_saved_articles(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            return SavedArticleManager(cursor).get_saved_articles(user_id)

    @staticmethod
    def delete_saved_article(user_id: str, article_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            return SavedArticleManager(cursor).delete_saved_article(user_id, article_id)