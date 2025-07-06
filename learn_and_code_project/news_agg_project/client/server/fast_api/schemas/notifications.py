from pydantic import BaseModel
from typing import List

class CategoryPreferenceRequest(BaseModel):
    user_id: str
    category: str
    enabled: bool

class KeywordUpdateRequest(BaseModel):
    user_id: str
    keywords: List[str]

class NotificationViewRequest(BaseModel):
    user_id: str
    article_id: str

class MarkAllViewedRequest(BaseModel):
    user_id: str
