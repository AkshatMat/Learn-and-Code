from core.interfaces import Checkbox

class MacOSCheckbox(Checkbox):    
    def render(self) -> str:
        status = "checked" if self._checked else "unchecked"
        return f"Rendering a MacOS-style checkbox ({status})"
    
    def toggle(self) -> str:
        self._checked = not self._checked
        status = "checked" if self._checked else "unchecked"
        return f"MacOS checkbox toggled to {status}"