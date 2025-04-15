from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class PaymentReceiver(ABC):
    @abstractmethod
    def receive_payment(self, amount: float) -> None:
        pass

class MoneyContainer(ABC):
    @abstractmethod
    def get_balance(self) -> float:
        pass
    
    @abstractmethod
    def add(self, amount: float) -> None:
        pass
    
    @abstractmethod
    def subtract(self, amount: float) -> None:
        pass