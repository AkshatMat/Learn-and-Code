from fastapi import APIRouter, HTTPException
from client.services.api_service import APIService
from client.server.fast_api.schemas.admin_schemas import APIUpsertRequest, APIStatusRequest, APIDeleteRequest
from client.utils.exception import ServiceError

router = APIRouter()

@router.get("/")
def get_all_apis():
    try:
        apis = APIService.get_all_apis()
        return {"apis": apis}
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{api_name}")
def get_api_by_name(api_name: str):
    try:
        api = APIService.get_api_by_name(api_name)
        if not api:
            raise HTTPException(status_code=404, detail=f"API '{api_name}' not found")
        return {"api": api}
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/")
def upsert_api(request: APIUpsertRequest):
    try:
        APIService.upsert_api(
            api_url=request.api_url,
            status=request.status,
            api_key=request.api_key,
            name=request.name
        )
        return {"message": f"API '{request.name}' updated successfully"}
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/")
def delete_api(request: APIDeleteRequest):
    try:
        success = APIService.delete_api(request.api_url)
        if success:
            return {"message": f"API with URL '{request.api_url}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"API with URL '{request.api_url}' not found")
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/status")
def update_api_status(request: APIStatusRequest):
    try:
        success = APIService.update_api_status(request.api_name, request.status)
        if success:
            return {"message": f"API '{request.api_name}' status updated to '{request.status}'"}
        else:
            raise HTTPException(status_code=404, detail=f"API '{request.api_name}' not found")
    except ServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 