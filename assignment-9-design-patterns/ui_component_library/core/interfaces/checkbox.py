from abc import ABC, abstractmethod

class Checkbox(ABC):
    def __init__(self):
        self._checked = False
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def toggle(self) -> str:
        pass
    
    @property
    def is_checked(self) -> bool:
        return self._checked