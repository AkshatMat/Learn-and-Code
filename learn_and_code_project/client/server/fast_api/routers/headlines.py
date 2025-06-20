from fastapi import APIRouter, HTTPException, Query
from client.services.headlines_service import HeadlinesService
from client.server.fast_api.schemas.headlines import HeadlinesRangeRequest
from client.services.headlines_service import HeadlinesService
from datetime import date
import pprint

router = APIRouter()

@router.get("/today")
def get_today_headlines(category: str = Query(default="All")):
    try:
        today = date.today().isoformat()
        HeadlinesService.get_headlines(today, today, category)
        return HeadlinesService.get_headlines(today, today, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/range")
def get_range_headlines(request: HeadlinesRangeRequest):
    try:
        return HeadlinesService.get_headlines(request.start_date, request.end_date, request.category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
def search_headlines(keyword: str = Query(..., min_length=1)):
    try:
        return HeadlinesService.search_headlines_by_keyword(keyword)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))