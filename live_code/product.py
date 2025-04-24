from typing import Dict, Any, Optional

class Product:
    def __init__(self, product_data: Dict[str, Any]):
        self.id = product_data.get('id')
        self.name = product_data.get('name')
        self.price = product_data.get('price', 0.0)
        self.description = product_data.get('description')
        self.category = product_data.get('category')
        self.stock = product_data.get('stock', 0)
        self.is_active = product_data.get('is_active', True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'stock': self.stock,
            'is_active': self.is_active
        }

    def reduce_stock(self, quantity: int) -> bool:
        if quantity > self.stock:
            return False
        
        self.stock -= quantity
        return True

    def add_stock(self, quantity: int) -> None:
        self.stock += quantity