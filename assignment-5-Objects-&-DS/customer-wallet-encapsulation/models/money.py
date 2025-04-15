from interfaces.payment import MoneyContainer
from exceptions.payment_exceptions import InsufficientFundsError

class Wallet(MoneyContainer):
    def __init__(self, initial_value: float = 0.0):
        if initial_value < 0:
            raise ValueError("Initial wallet value cannot be negative")
        self._value = initial_value
    
    def get_balance(self) -> float:
        return self._value
    
    def add(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount to add must be positive")
        self._value += amount
    
    def subtract(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount to subtract must be positive")
        if amount > self._value:
            raise InsufficientFundsError(f"Insufficient funds: {self._value} available, {amount} requested")
        self._value -= amount