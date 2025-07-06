from pydantic import BaseModel
from uuid import UUID

class SaveArticleRequest(BaseModel):
    user_id: str
    article_id: str

class DeleteArticleRequest(BaseModel):
    user_id: UUID
    article_id: UUID
