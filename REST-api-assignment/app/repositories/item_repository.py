from typing import Dict, List
from datetime import datetime
from fastapi import HTTPException

class ItemRepository:
    def __init__(self):
        self.db: Dict[int, dict] = {}
        self.counter = 1
    
    def create(self, item_dict: dict) -> dict:
        item_dict["id"] = self.counter
        item_dict["created_at"] = datetime.now()
        item_dict["updated_at"] = None
        
        self.db[self.counter] = item_dict
        self.counter += 1
        return item_dict
    
    def get_all(self) -> List[dict]:
        return list(self.db.values())
    
    def get_by_id(self, item_id: int) -> dict:
        if item_id not in self.db:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        return self.db[item_id]
    
    def update(self, item_id: int, update_data: dict) -> dict:
        if item_id not in self.db:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        
        stored_item = self.db[item_id]
        
        for key, value in update_data.items():
            if value is not None:
                stored_item[key] = value
        
        stored_item["updated_at"] = datetime.now()
        return stored_item
    
    def delete(self, item_id: int) -> None:
        if item_id not in self.db:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        del self.db[item_id]