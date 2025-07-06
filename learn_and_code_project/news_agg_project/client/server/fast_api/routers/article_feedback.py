from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from client.services.feedback_service import FeedbackService
from client.server.fast_api.schemas.feedback import FeedbackRequest

router = APIRouter()

@router.post("/feedback")
def give_feedback(request: FeedbackRequest):
    try:
        if request.feedback not in ['like', 'dislike']:
            raise ValueError("Feedback must be 'like' or 'dislike'")
        FeedbackService.give_feedback(request.user_id, request.article_id, request.feedback)
        return {"message": f"Article {request.feedback}d successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
