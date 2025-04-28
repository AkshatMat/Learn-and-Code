from typing import Dict, Any, Optional

class Customer:
    def __init__(self, customer_data: Dict[str, Any]):
        self.id = customer_data.get('id')
        self.name = customer_data.get('name')
        self.email = customer_data.get('email')
        self.address = customer_data.get('address')
        self.phone = customer_data.get('phone')
        self.membership_level = customer_data.get('membership_level')
        self.order_history = customer_data.get('order_history', [])

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
            'membership_level': self.membership_level,
            'order_history': self.order_history
        }

    def update_order_history(self, order_id: str) -> None:
        self.order_history.append(order_id)