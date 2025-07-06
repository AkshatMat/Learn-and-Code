from fastapi import APIRouter, HTTPException
from client.services.notification_service import NotificationService
from client.server.fast_api.schemas.notifications import (
    CategoryPreferenceRequest,
    KeywordUpdateRequest,
    NotificationViewRequest,
    MarkAllViewedRequest
)

router = APIRouter()

@router.get("/preferences/{user_id}")
def get_user_preferences(user_id: str):
    try:
        return NotificationService.get_user_preferences(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preferences/category")
def update_category_preference(request: CategoryPreferenceRequest):
    try:
        NotificationService.update_category_preference(request.user_id, request.category, request.enabled)
        return {"message": "Category preference updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences/keywords/{user_id}")
def get_keywords(user_id: str):
    try:
        return NotificationService.get_keywords(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preferences/keywords")
def update_keywords(request: KeywordUpdateRequest):
    try:
        NotificationService.update_keywords(request.user_id, request.keywords)
        return {"message": "Keywords updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences/unviewed/{user_id}")
def get_unviewed_notifications(user_id: str):
    print("In router.notifications!!!!")
    try:
        return NotificationService.get_unviewed_notifications(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/viewed")
def mark_notification_as_viewed(request: NotificationViewRequest):
    try:
        NotificationService.mark_notification_as_viewed(request.user_id, request.article_id)
        return {"message": "Notification marked as viewed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/viewed_all")
def mark_all_as_viewed(request: MarkAllViewedRequest):
    try:
        NotificationService.mark_all_as_viewed(request.user_id)
        return {"message": "All notifications marked as viewed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
