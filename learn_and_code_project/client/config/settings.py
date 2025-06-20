import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = "http://127.0.0.1:8000"
    CATEGORIES: List[str] = [
        'general', 'science', 'sports', 'business', 
        'health', 'entertainment', 'technology', 'politics'
    ]
    
    DB_NAME: str = os.getenv("DB_NAME", "news_agg")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    
    DB_MIN_CONNECTIONS: int = 1
    DB_MAX_CONNECTIONS: int = 10
    
    MIN_CONTENT_LENGTH: int = 200
    REQUEST_TIMEOUT: int = 10

settings = Settings()
