from client.db.connection import DatabaseConnection
from client.db.modules.news_manager import NewsManager

class HeadlinesService:
    @staticmethod
    def get_headlines(start_date: str, end_date: str, category: str = "All"):
        with DatabaseConnection.get_cursor() as cursor:
            return NewsManager(cursor).fetch_headlines(start_date, end_date, category)
        
    @staticmethod
    def search_headlines_by_keyword(keyword: str):
        with DatabaseConnection.get_cursor() as cursor:
            return NewsManager(cursor).search_articles_by_keyword(keyword)
