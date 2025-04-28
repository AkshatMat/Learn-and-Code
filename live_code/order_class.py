from typing import Dict, List, Any
from datetime import datetime

class Order:
    def __init__(self, order_data: Dict[str, Any]):
        self.id = order_data.get('id')
        self.customer_id = order_data.get('customer_id')
        self.items = order_data.get('items', [])
        self.total_amount = order_data.get('total_amount', 0.0)
        self.status = order_data.get('status', 'pending')
        self.created_at = order_data.get('created_at', datetime.now().isoformat())
        self.updated_at = order_data.get('updated_at', self.created_at)
        self.discount_applied = order_data.get('discount_applied', 0.0)
        self.final_amount = order_data.get('final_amount', self.total_amount)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'discount_applied': self.discount_applied,
            'final_amount': self.final_amount
        }

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.updated_at = datetime.now().isoformat()

    def apply_discount(self, discount_amount: float) -> None:
        self.discount_applied = discount_amount
        self.final_amount = self.total_amount - discount_amount