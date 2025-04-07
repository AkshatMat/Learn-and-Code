from typing import List
from app.models.item import Item, ItemCreate, ItemUpdate
from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self):
        self.repository = ItemRepository()
    
    def create_item(self, item: ItemCreate) -> Item:
        item_dict = self.repository.create(item.dict())
        return Item(**item_dict)
    
    def get_items(self) -> List[Item]:
        items = self.repository.get_all()
        return [Item(**item) for item in items]
    
    def get_item(self, item_id: int) -> Item:
        item_dict = self.repository.get_by_id(item_id)
        return Item(**item_dict)
    
    def update_item(self, item_id: int, item: ItemUpdate) -> Item:
        update_data = item.dict(exclude_unset=True)
        item_dict = self.repository.update(item_id, update_data)
        return Item(**item_dict)
    
    def delete_item(self, item_id: int) -> None:
        self.repository.delete(item_id)