from core.interfaces import Button

class MacOSButton(Button):
    def render(self) -> str:
        return "Rendering a MacOS-style button"
    
    def on_click(self) -> str:
        return "MacOS button clicked!"