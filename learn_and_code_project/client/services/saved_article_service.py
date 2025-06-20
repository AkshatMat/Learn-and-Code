from db.connection import DatabaseConnection
from db.modules.saved_article_manager import SavedArticleManager

class SavedArticleService:
    def save(self, user_id, article_id):
        with DatabaseConnection.get_cursor() as cursor:
            SavedArticleManager(cursor).save_article(user_id, article_id)

    def delete(self, user_id, article_id):
        with DatabaseConnection.get_cursor() as cursor:
            SavedArticleManager(cursor).delete_saved_article(user_id, article_id)

    def fetch_all(self, user_id):
        with DatabaseConnection.get_cursor() as cursor:
            return SavedArticleManager(cursor).get_saved_articles(user_id)
