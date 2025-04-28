from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

item_service = ItemService()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    try:
        return item_service.create_item(item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Item])
def read_items():
    try:
        return item_service.get_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int):
    try:
        return item_service.get_item(item_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    try:
        return item_service.update_item(item_id, item)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    try:
        item_service.delete_item(item_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))