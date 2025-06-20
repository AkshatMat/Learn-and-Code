from client.db.connection import DatabaseConnection
from client.db.modules.news_manager import NewsManager
from datetime import datetime

class NewsService:
    @staticmethod
    def get_today_headlines(category="All"):
        today = datetime.today().date()
        with DatabaseConnection.get_cursor() as cursor:
            return NewsManager(cursor).fetch_headlines(str(today), str(today), category)

    @staticmethod
    def get_range_headlines(start_date: str, end_date: str, category="All"):
        with DatabaseConnection.get_cursor() as cursor:
            return NewsManager(cursor).fetch_headlines(start_date, end_date, category)