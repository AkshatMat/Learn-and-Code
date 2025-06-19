from abc import ABC, abstractmethod
from typing import List, Optional
from models.news_article import NewsArticle

class BaseRepository(ABC):
    @abstractmethod
    def save(self, article: NewsArticle) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, article_id: str) -> Optional[NewsArticle]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[NewsArticle]:
        pass
    
    @abstractmethod
    def delete(self, article_id: str) -> bool:
        pass