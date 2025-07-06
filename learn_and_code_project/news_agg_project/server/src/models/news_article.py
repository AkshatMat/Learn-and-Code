import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class NewsArticle:
    title: str
    source: str
    url: str
    category: str
    author: Optional[str] = None
    published_at: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    full_title: Optional[str] = None
    full_content: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("Title is required")
        if not self.url:
            raise ValueError("URL is required")
        if not self.category:
            raise ValueError("Category is required")