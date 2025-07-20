from core.interfaces import Button

class WindowsButton(Button):    
    def render(self) -> str:
        return "Rendering a Windows-style button"
    
    def on_click(self) -> str:
        return "Windows button clicked!"