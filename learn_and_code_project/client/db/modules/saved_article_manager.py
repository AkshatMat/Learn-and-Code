from client.utils.logger import logger
from client.utils.exception import DatabaseError

class SavedArticleManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_saved_articles(self, user_id: str):
        try:
            query = """
                SELECT a.uuid, a.title, a.content, a.source, a.url, a.category
                FROM saved_article_table s
                JOIN news_table a ON s.article_id = a.uuid
                WHERE s.user_id = %s
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching saved articles: {e}")
            raise DatabaseError("Failed to fetch saved articles")

    def save_article(self, user_id: str, article_id: str):
        try:
            insert_query = """
                INSERT INTO saved_article_table (user_id, article_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cursor.execute(insert_query, (user_id, article_id))
            logger.info("Article saved successfully.")
        except Exception as e:
            logger.error(f"Error saving article: {e}")
            raise DatabaseError("Failed to save article")

    def delete_saved_article(self, user_id: str, article_id: str):
        try:
            delete_query = """
                DELETE FROM saved_article_table
                WHERE user_id = %s AND article_id = %s;
            """
            self.cursor.execute(delete_query, (user_id, article_id))
            logger.info("Saved article deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting saved article: {e}")
            raise DatabaseError("Failed to delete saved article")
