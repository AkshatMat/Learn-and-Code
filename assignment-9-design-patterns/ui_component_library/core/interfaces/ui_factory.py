from abc import ABC, abstractmethod
from core.interfaces.button import Button
from core.interfaces.checkbox import Checkbox
from core.interfaces.text_field import TextField

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass