from typing import Optional
from utils.exception import ValidationError
from config.settings import settings

class ArticleValidator:    
    @staticmethod
    def contains_ssl_warning(content: str) -> bool:
        patterns = [
            "This server could not prove that it is",
            "its security certificate is not trusted",
            "Proceed to",
            "-----BEGIN CERTIFICATE-----"
        ]
        return any(pattern in content for pattern in patterns)
    
    @staticmethod
    def is_valid_article(
        title: Optional[str], 
        content: Optional[str], 
        published_at: Optional[str]
    ) -> bool:
        try:
            if not title or "just a moment" in title.lower():
                return False
            
            if not content:
                return False
                
            content_lower = content.lower()
            if "verifying you are human" in content_lower:
                return False
                
            if len(content.strip()) < settings.MIN_CONTENT_LENGTH:
                return False
            
            if ArticleValidator.contains_ssl_warning(content):
                return False
            
            if not published_at:
                return False
                
            return True
            
        except Exception as e:
            raise ValidationError(f"Article validation failed: {str(e)}")