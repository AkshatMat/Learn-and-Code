import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CATEGORIES: List[str] = [
        'general', 'science', 'sports', 'business', 
        'health', 'entertainment', 'technology', 'politics'
    ]
    
    OUTPUT_DIR: str = "output"
    
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    
    NEWS_PER_CATEGORY = 1
    
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
    BEDROCK_TEMPERATURE: float = float(os.getenv("BEDROCK_TEMPERATURE", "0.1"))
    
    DB_NAME: str = os.getenv("DB_NAME", "news_agg")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    
    DB_MIN_CONNECTIONS: int = 1
    DB_MAX_CONNECTIONS: int = 10
    
    MIN_CONTENT_LENGTH: int = 200
    REQUEST_TIMEOUT: int = 10
    
    def __post_init__(self):
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

settings = Settings()
settings.__post_init__()  