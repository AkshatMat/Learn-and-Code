import requests
from typing import List
from models.news_article import NewsArticle
from repositories.database_repository import DatabaseRepository
from config.settings import settings
from utils.exception import NewsAPIError, ConfigurationError
from utils.logger import logger

class AlternativeNewsAPIService:
    def __init__(self):
        self.db = DatabaseRepository()
        fallback_api_config = self.db.get_fallbackapi_entry()
        self.api_key = fallback_api_config['api_key']
        self.base_url = fallback_api_config['api_url']
        if not self.api_key:
            raise ConfigurationError("THE_NEWS_API_KEY is required")
        
    def fetch_top_headlines(
        self, 
        category: str, 
        country: str = "us", 
        language: str = "en", 
        page_size: int = 1
    ) -> List[NewsArticle]:
        try:
            logger.info(f"Fetching {category} headlines from Alternative News API")
            response = requests.get(
                self.base_url,
                params={
                    "category": category,
                    "country": country,
                    "language": language,
                    "limit": page_size,
                    "apiKey": self.api_key
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article_data in data.get("articles", []):
                article = NewsArticle(
                    title=article_data.get("title", ""),
                    source=article_data.get("source", {}).get("name", ""),
                    url=article_data.get("url", ""),
                    author=article_data.get("author"),
                    published_at=article_data.get("publishedAt"),
                    category=category
                )
                articles.append(article)
                
            logger.info(f"Successfully fetched {len(articles)} articles from fallback API")
            
            self.db.update_api_last_accessed("TheNewsAPI")
            return articles
        
        except Exception as e:
            self.db.update_api_status("TheNewsAPI", "In-active")
            raise NewsAPIError(f"Fallback API failed: {str(e)}")