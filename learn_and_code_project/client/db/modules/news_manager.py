from datetime import datetime
from client.utils.logger import logger
from client.utils.exception import DatabaseError

class NewsManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_headlines(self, start_date: str, end_date: str, category: str = None):
        try:
            query = """
                SELECT uuid, title, content, source, category, published_at, url, author
                FROM news_table
                WHERE published_at BETWEEN %s AND %s
            """
            params = [start_date, end_date]

            if category and category.lower() != "all":
                query += " AND LOWER(category) = LOWER(%s)"
                params.append(category)

            query += " ORDER BY published_at DESC"
            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()

        except Exception as e:
            logger.error(f"Error fetching headlines: {e}")
            raise DatabaseError("Failed to fetch headlines")

    def search_articles_by_keyword(self, keyword: str):
        query = """
            SELECT uuid, title, content, source, url, category
            FROM news_table
            WHERE LOWER(keywords::text) LIKE LOWER(%s)
            ORDER BY published_at DESC;
        """
        self.cursor.execute(query, (f'%{keyword}%',))
        return self.cursor.fetchall()