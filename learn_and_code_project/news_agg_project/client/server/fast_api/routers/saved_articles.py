from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from client.services.user_service import UserService
from client.server.fast_api.schemas.saved_article import SaveArticleRequest

router = APIRouter()

@router.get("/saved_articles/{user_id}")
def get_saved_articles(user_id: str):
    try:
        return UserService.get_saved_articles(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save_article")
def save_article(request: SaveArticleRequest):
    try:
        UserService.save_article(request.user_id, request.article_id)
        return {"message": "Article saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_article")
def delete_article(request: SaveArticleRequest):
    try:
        UserService.delete_saved_article(request.user_id, request.article_id)
        return {"message": "Article deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
