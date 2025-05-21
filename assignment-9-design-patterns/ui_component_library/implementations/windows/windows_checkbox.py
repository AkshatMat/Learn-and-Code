from core.interfaces import Checkbox

class WindowsCheckbox(Checkbox):    
    def render(self) -> str:
        status = "checked" if self._checked else "unchecked"
        return f"Rendering a Windows-style checkbox ({status})"
    
    def toggle(self) -> str:
        self._checked = not self._checked
        status = "checked" if self._checked else "unchecked"
        return f"Windows checkbox toggled to {status}"