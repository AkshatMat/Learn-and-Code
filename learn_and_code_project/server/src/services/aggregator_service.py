import time
from typing import List, Dict, Any
from models.news_article import NewsArticle
from services.news_api_service import NewsAPIService
from services.scraper_service import ScraperService
from services.keyword_extraction_service import KeywordExtractionService
from repositories.database_repository import DatabaseRepository
from repositories.file_repository import FileRepository
from utils.validators import ArticleValidator
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

class AggregatorService:
    def __init__(self):
        self.news_api_service = NewsAPIService()
        self.scraper_service = ScraperService()
        self.keyword_service = KeywordExtractionService()
        self.db_repository = DatabaseRepository()
        self.file_repository = FileRepository()
        
    def aggregate_news(self) -> Dict[str, Any]:
        logger.info("Starting news aggregation process")
        all_articles = []
        category_stats = {}
        
        for category in settings.CATEGORIES:
            logger.info(f"Processing category: {category.upper()}")
            
            try:
                articles = self.news_api_service.fetch_top_headlines(
                    category=category,
                    country="us",
                    language="en"
                )
                
                if not articles:
                    logger.warning(f"No articles found for category: {category}")
                    category_stats[category] = 0
                    continue
                
                processed_count = 0
                
                for idx, article in enumerate(articles, settings.NEWS_PER_CATEGORY):
                    logger.info(f"[{category.upper()} - {idx}] Processing: {article.title}")
                    
                    if self._process_single_article(article):
                        all_articles.append(article)
                        processed_count += 1
                        logger.info(f"Successfully processed article: {article.id}")
                    else:
                        logger.warning(f"Failed to process article: {article.title}")
                    
                    time.sleep(1)
                
                category_stats[category] = processed_count
                logger.info(f"Completed category {category}: {processed_count} articles processed")
                
            except Exception as e:
                logger.error(f"Error processing category {category}: {str(e)}")
                category_stats[category] = 0
                continue
        
        total_articles = len(all_articles)
        
        results = {
            "total_articles": total_articles,
            "category_stats": category_stats,
            "articles": all_articles,
            "success": total_articles > 0
        }
        
        logger.info(f"News aggregation completed. Total articles: {total_articles}")
        self._log_category_stats(category_stats)
        
        return results
    
    def _process_single_article(self, article: NewsArticle) -> bool:
        try:
            scraper_result = self.scraper_service.extract_article(article.url)
            
            if not scraper_result:
                logger.warning(f"Failed to extract content for: {article.url}")
                return False
            
            full_title, content, scraper_keywords = scraper_result
            
            if not ArticleValidator.is_valid_article(full_title, content, article.published_at):
                logger.warning(f"Article validation failed for: {article.title}")
                return False
            
            article.full_title = full_title
            article.full_content = content.strip()
            
            keywords = self.keyword_service.extract_keywords(content)
            article.keywords = keywords if keywords else scraper_keywords
            
            if keywords:
                logger.info(f"LLM extracted keywords: {keywords}")
            else:
                logger.info("Using scraper keywords as fallback")
                article.keywords = scraper_keywords
            
            db_success = self.db_repository.save(article)
            file_success = self.file_repository.save_article(article)
            
            if db_success:
                logger.info(f"Article saved to database: {article.id}")
            else:
                logger.warning(f"Failed to save article to database: {article.id}")
            
            if file_success:
                logger.info(f"Article saved to file: {article.id}")
            else:
                logger.warning(f"Failed to save article to file: {article.id}")
            
            return db_success or file_success 
            
        except Exception as e:
            logger.error(f"Error processing article {article.id}: {str(e)}")
            return False
    
    def _log_category_stats(self, category_stats: Dict[str, int]) -> None:
        logger.info("Articles processed by category:")
        for category, count in category_stats.items():
            logger.info(f"  {category.capitalize()}: {count} articles")
    
    def get_aggregation_summary(self, results: Dict[str, Any]) -> str:
        if not results["success"]:
            return "News aggregation completed with no articles processed."
        
        summary_lines = [
            "=" * 60,
            "NEWS AGGREGATION SUMMARY",
            "=" * 60,
            f"Total articles processed: {results['total_articles']}",
            "",
            "Articles by category:"
        ]
        
        for category, count in results["category_stats"].items():
            summary_lines.append(f"  {category.capitalize()}: {count} articles")
        
        summary_lines.extend([
            "",
            "=" * 60
        ])
        
        return "\n".join(summary_lines)
    
    def cleanup_resources(self) -> None:
        try:
            self.db_repository.close_connection()
            logger.info("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")