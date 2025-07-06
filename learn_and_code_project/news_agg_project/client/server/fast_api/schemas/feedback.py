from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    user_id: str
    article_id: str
    feedback: str 
