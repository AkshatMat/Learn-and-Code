import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from repositories.base_repository import BaseRepository
from models.news_article import NewsArticle
from utils.logger import setup_logger
from utils.exception import RepositoryError
from config.settings import settings

logger = setup_logger(__name__)

class FileRepository(BaseRepository):
    def __init__(self, output_directory: str = None):
        self.output_dir = output_directory or settings.OUTPUT_DIR
        self._ensure_output_directory()
    
    def _ensure_output_directory(self) -> None:
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.debug(f"Output directory ensured: {self.output_dir}")
        except Exception as e:
            raise RepositoryError(f"Failed to create output directory {self.output_dir}: {str(e)}")
    
    def save_article(self, article: NewsArticle) -> bool:
        try:
            data = self._article_to_dict(article)
            filepath = self._get_article_filepath(article.id)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, default=str)
            
            logger.debug(f"Article saved to file: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving article {article.id} to file: {str(e)}")
            return False
    
    def get_article_by_id(self, article_id: str) -> Optional[NewsArticle]:
        try:
            filepath = self._get_article_filepath(article_id)
            
            if not os.path.exists(filepath):
                logger.debug(f"Article file not found: {filepath}")
                return None
            
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            return self._dict_to_article(data)
            
        except Exception as e:
            logger.error(f"Error loading article {article_id} from file: {str(e)}")
            return None
    
    def get_articles_by_category(self, category: str) -> List[NewsArticle]:
        articles = []
        
        try:
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.json'):
                    article_id = filename[:-5]  
                    article = self.get_article_by_id(article_id)
                    
                    if article and article.category == category:
                        articles.append(article)
            
            logger.debug(f"Found {len(articles)} articles in category: {category}")
            return articles
            
        except Exception as e:
            logger.error(f"Error getting articles by category {category}: {str(e)}")
            return []
    
    def get_all_articles(self) -> List[NewsArticle]:
        articles = []
        
        try:
            if not os.path.exists(self.output_dir):
                logger.debug(f"Output directory doesn't exist: {self.output_dir}")
                return articles
            
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.json'):
                    article_id = filename[:-5]  
                    article = self.get_article_by_id(article_id)
                    
                    if article:
                        articles.append(article)
            
            logger.debug(f"Loaded {len(articles)} articles from files")
            return articles
            
        except Exception as e:
            logger.error(f"Error getting all articles: {str(e)}")
            return []
    
    def delete_article(self, article_id: str) -> bool:
        try:
            filepath = self._get_article_filepath(article_id)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"Article file deleted: {filepath}")
                return True
            else:
                logger.debug(f"Article file not found for deletion: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting article {article_id}: {str(e)}")
            return False
    
    def update_article(self, article: NewsArticle) -> bool:
        return self.save_article(article)
    
    def clear_all_articles(self) -> bool:
        try:
            if not os.path.exists(self.output_dir):
                logger.debug(f"Output directory doesn't exist: {self.output_dir}")
                return True
            
            deleted_count = 0
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.output_dir, filename)
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Error deleting file {filepath}: {str(e)}")
            
            logger.info(f"Cleared {deleted_count} article files")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing all articles: {str(e)}")
            return False
    
    def get_articles_count(self) -> int:
        try:
            if not os.path.exists(self.output_dir):
                return 0
            
            count = sum(1 for filename in os.listdir(self.output_dir) 
                       if filename.endswith('.json'))
            
            return count
            
        except Exception as e:
            logger.error(f"Error counting articles: {str(e)}")
            return 0
    
    def get_articles_by_date_range(self, start_date: datetime, end_date: datetime) -> List[NewsArticle]:
        articles = []
        
        try:
            all_articles = self.get_all_articles()
            
            for article in all_articles:
                if article.published_at:
                    if isinstance(article.published_at, str):
                        try:
                            pub_date = datetime.fromisoformat(article.published_at.replace('Z', '+00:00'))
                        except:
                            continue
                    else:
                        pub_date = article.published_at
                    
                    if start_date <= pub_date <= end_date:
                        articles.append(article)
            
            logger.debug(f"Found {len(articles)} articles in date range")
            return articles
            
        except Exception as e:
            logger.error(f"Error getting articles by date range: {str(e)}")
            return []
    
    def get_repository_stats(self) -> Dict[str, Any]:
        try:
            total_articles = self.get_articles_count()
            
            category_stats = {}
            all_articles = self.get_all_articles()
            
            for article in all_articles:
                category = article.category or 'unknown'
                category_stats[category] = category_stats.get(category, 0) + 1
            
            total_size = 0
            if os.path.exists(self.output_dir):
                for filename in os.listdir(self.output_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.output_dir, filename)
                        total_size += os.path.getsize(filepath)
            
            return {
                "total_articles": total_articles,
                "category_distribution": category_stats,
                "total_size_bytes": total_size,
                "output_directory": self.output_dir
            }
            
        except Exception as e:
            logger.error(f"Error getting repository stats: {str(e)}")
            return {"error": str(e)}
    
    def _article_to_dict(self, article: NewsArticle) -> Dict[str, Any]:
        return {
            "id": article.id,
            "title": article.full_title or article.title,
            "author": article.author,
            "published_at": article.published_at,
            "category": article.category,
            "keywords": article.keywords,
            "url": article.url,
            "source": article.source,
            "content": article.full_content,
            "created_at": datetime.now().isoformat()
        }
    
    def _dict_to_article(self, data: Dict[str, Any]) -> NewsArticle:
        article = NewsArticle(
            title=data.get("title", ""),
            source=data.get("source", ""),
            url=data.get("url", ""),
            author=data.get("author"),
            published_at=data.get("published_at"),
            category=data.get("category", "")
        )
        
        article.id = data.get("id", article.id)
        article.full_title = data.get("title")
        article.full_content = data.get("content")
        article.keywords = data.get("keywords", [])
        
        return article
    
    def _get_article_filepath(self, article_id: str) -> str:
        return os.path.join(self.output_dir, f"{article_id}.json")
    
    def save(self, article: NewsArticle) -> bool:
        return self.save_article(article)

    def get_by_id(self, article_id: str) -> Optional[NewsArticle]:
        return self.get_article_by_id(article_id)

    def get_all(self) -> List[NewsArticle]:
        return self.get_all_articles()

    def delete(self, article_id: str) -> bool:
        return self.delete_article(article_id)
    
    def close_connection(self) -> None:
        logger.debug("File repository connection closed (no-op)")