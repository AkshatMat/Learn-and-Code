import requests
from typing import List
from models.news_article import NewsArticle
from services.alternative_news_api_service import AlternativeNewsAPIService
from repositories.database_repository import DatabaseRepository
from config.settings import settings
from utils.exception import NewsAPIError, ConfigurationError
from utils.logger import logger

class NewsAPIService:    
    def __init__(self):
        self.db = DatabaseRepository()
        entry_api_config = self.db.get_newsapi_entry()
        self.api_key = entry_api_config['api_key']
        self.base_url = entry_api_config['api_url']
        if not self.api_key:
            raise ConfigurationError("NEWS_API_KEY is required")
        self.fallback_service = AlternativeNewsAPIService()
        
    def fetch_top_headlines(self, category: str, country: str = "us", language: str = "en", page_size: int = 1) -> List[NewsArticle]:        
        params = {
            "category": category,
            "country": country,
            "language": language,
            "apiKey": self.api_key,
            "pageSize": page_size
        }
        
        try:
            logger.info(f"Fetching {category} headlines from News API")
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=settings.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            articles_data = data.get("articles", [])
            
            articles = []
            for article_data in articles_data:
                try:
                    article = NewsArticle(
                        title=article_data.get("title", ""),
                        source=article_data.get("source", {}).get("name", ""),
                        url=article_data.get("url", ""),
                        author=article_data.get("author"),
                        published_at=article_data.get("publishedAt"),
                        category=category
                    )
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to create article from data: {str(e)}")
                    continue
            
            logger.info(f"Successfully fetched {len(articles)} articles for {category}")
            
            self.db.update_api_last_accessed("NewsAPI")
            
            return articles
            
        except requests.RequestException as e:
            raise NewsAPIError(f"Failed to fetch headlines for {category}: {str(e)}")
        
        except Exception as e:
            self.db.update_api_status("NewsAPI", "In-active")
            logger.error(f"Primary API failed: {str(e)}. Trying fallback...")
            return self.fallback_service.fetch_top_headlines(
                category, country, language, page_size
            )