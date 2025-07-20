from abc import ABC, abstractmethod

class TextField(ABC):    
    def __init__(self):
        self._text = ""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def on_text_changed(self, new_text: str) -> str:
        pass
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self.on_text_changed(value)