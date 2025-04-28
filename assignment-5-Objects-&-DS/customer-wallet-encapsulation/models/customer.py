from typing import Optional
from models.person import Person
from models.money import Wallet
from interfaces.payment import PaymentProcessor, PaymentReceiver, MoneyContainer
from exceptions.payment_exceptions import InsufficientFundsError

class Customer(Person, PaymentProcessor, PaymentReceiver):    
    def __init__(self, first_name: str, last_name: str, wallet: Optional[MoneyContainer] = None):
        super().__init__(first_name, last_name)
        self._wallet = wallet if wallet is not None else Wallet()
    
    def get_wallet_balance(self) -> float:
        return self._wallet.get_balance()
    
    def process_payment(self, amount: float) -> bool:
        try:
            if amount <= 0:
                raise ValueError("Payment amount must be positive")
            self._wallet.subtract(amount)
            return True
        except InsufficientFundsError:
            return False
    
    def receive_payment(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        self._wallet.add(amount)