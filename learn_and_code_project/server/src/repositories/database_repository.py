from typing import List, Optional
from datetime import datetime, timezone, timedelta
import psycopg2
from repositories.base_repository import BaseRepository
from models.news_article import NewsArticle
from database.connection import DatabaseConnection
from utils.exception import DatabaseError
from utils.logger import logger

class DatabaseRepository(BaseRepository):    
    def __init__(self):
        self._ensure_table_exists()
    
    def _ensure_table_exists(self) -> None:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS news_table (
                        uuid UUID PRIMARY KEY,
                        published_at TIMESTAMP,
                        category TEXT,
                        keywords TEXT[],
                        content TEXT,
                        title TEXT,
                        author TEXT,
                        source TEXT,
                        url TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                cursor.execute(create_table_query)
                logger.info("Database table ensured to exist")
        except Exception as e:
            raise DatabaseError(f"Failed to create table: {str(e)}")
    
    def save(self, article: NewsArticle) -> bool:
        try:
            published_at = self._parse_published_date(article.published_at)
            
            with DatabaseConnection.get_cursor() as cursor:
                insert_query = """
                    INSERT INTO news_table (
                        uuid, published_at, category, keywords, content, 
                        title, author, source, url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (uuid) DO UPDATE SET
                        published_at = EXCLUDED.published_at,
                        category = EXCLUDED.category,
                        keywords = EXCLUDED.keywords,
                        content = EXCLUDED.content,
                        title = EXCLUDED.title,
                        author = EXCLUDED.author,
                        source = EXCLUDED.source,
                        url = EXCLUDED.url
                """
                
                cursor.execute(insert_query, (
                    article.id,
                    published_at,
                    article.category,
                    article.keywords,
                    article.full_content,
                    article.full_title or article.title,
                    article.author,
                    article.source,
                    article.url
                ))
                
            logger.info(f"Successfully saved article {article.id} to database")
            return True
            
        except Exception as e:
            logger.error(f"Error saving article {article.id} to database: {str(e)}")
            return False
    
    def get_by_id(self, article_id: str) -> Optional[NewsArticle]:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM news_table WHERE uuid = %s", 
                    (article_id,)
                )
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_article(row)
                return None
                
        except Exception as e:
            raise DatabaseError(f"Error fetching article {article_id}: {str(e)}")
    
    def get_all(self) -> List[NewsArticle]:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute("SELECT * FROM news_table ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                return [self._row_to_article(row) for row in rows]
                
        except Exception as e:
            raise DatabaseError(f"Error fetching all articles: {str(e)}")
    
    def delete(self, article_id: str) -> bool:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM news_table WHERE uuid = %s", 
                    (article_id,)
                )
                return cursor.rowcount > 0
                
        except Exception as e:
            raise DatabaseError(f"Error deleting article {article_id}: {str(e)}")
    
    def close_connection(self) -> None:
        try:
            DatabaseConnection.close_pool()
            logger.info("Database connection pool closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {str(e)}")
    
    def _parse_published_date(self, published_at_str: Optional[str]) -> Optional[datetime]:
        if not published_at_str:
            return None
        
        try:
            if 'T' in published_at_str:
                return datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
            else:
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                    try:
                        return datetime.strptime(published_at_str, fmt)
                    except ValueError:
                        continue
            return None
        except Exception as e:
            logger.warning(f"Error parsing date '{published_at_str}': {str(e)}")
            return None
    
    def _row_to_article(self, row) -> NewsArticle:
        article = NewsArticle(
            title=row['title'] or '',
            source=row['source'] or '',
            url=row['url'] or '',
            category=row['category'] or '',
            author=row['author'],
            published_at=row['published_at'].isoformat() if row['published_at'] else None
        )
        
        article.id = row['uuid']
        article.full_content = row['content']
        article.keywords = row['keywords'] or []
        
        return article
    
    def upsert_api_entry(self, api_url: str, status: str, api_key: str, name: str, last_accessed: Optional[datetime]) -> bool:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    INSERT INTO api_table (api_url, status, api_key, name, last_accessed)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (api_url) DO UPDATE SET
                        status = EXCLUDED.status,
                        api_key = EXCLUDED.api_key,
                        name = EXCLUDED.name,
                        last_accessed = EXCLUDED.last_accessed"""
                cursor.execute(query, (api_url, status, api_key, name, last_accessed))
            logger.info(f"Upserted API entry for URL: {api_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert API entry {api_url}: {str(e)}")
            return False
        
    def delete_api_entry(self, api_url: str) -> bool:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = "DELETE FROM api_table WHERE api_url = %s"
                cursor.execute(query, (api_url,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete API entry {api_url}: {str(e)}")
            return False
        
    def get_newsapi_entry(self) -> Optional[dict]:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = "SELECT * FROM api_table WHERE name = %s LIMIT 1"
                cursor.execute(query, ("NewsAPI",))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to fetch NewsAPI entry: {str(e)}")
            return None

    def get_fallbackapi_entry(self) -> Optional[dict]:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = "SELECT * FROM api_table WHERE name = %s LIMIT 1"
                cursor.execute(query, ("TheNewsAPI",))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to fetch FallbackAPI entry: {str(e)}")
            return None
        
    def update_api_last_accessed(self, api_name: str, timestamp: Optional[datetime] = None) -> bool:
        try:
            if not timestamp:
                timestamp = datetime.utcnow()
            
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    UPDATE api_table
                    SET last_accessed = %s
                    WHERE name = %s
                """
                cursor.execute(query, (timestamp, api_name))
            
            logger.info(f"Updated last_accessed for API '{api_name}' to {timestamp}")
            return True
        except Exception as e:
            logger.error(f"Failed to update last_accessed for API '{api_name}': {str(e)}")
            return False
    
    def update_api_last_accessed(self, api_name: str, timestamp: Optional[datetime] = None) -> bool:
        IST = timezone(timedelta(hours=5, minutes=30))
        try:
            if not timestamp:
                timestamp = datetime.now(IST) 
            
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    UPDATE api_table
                    SET last_accessed = %s
                    WHERE name = %s
                """
                cursor.execute(query, (timestamp, api_name))
            
            logger.info(f"Updated last_accessed for API '{api_name}' to {timestamp}")
            return True
        except Exception as e:
            logger.error(f"Failed to update last_accessed for API '{api_name}': {str(e)}")
            return False
        
    def update_api_status(self, api_name: str, status: str = "Active") -> bool:
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    UPDATE api_table
                    SET status = %s
                    WHERE name = %s
                """
                cursor.execute(query, (status, api_name))
            
            logger.info(f"Updated status for API '{api_name}' to {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update status for API '{api_name}': {str(e)}")
            return False