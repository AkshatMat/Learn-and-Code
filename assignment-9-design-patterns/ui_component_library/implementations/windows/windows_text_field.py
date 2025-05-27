from core.interfaces import TextField

class WindowsTextField(TextField):
    def render(self) -> str:
        return f"Rendering a Windows-style text field with text: '{self._text}'"
    
    def on_text_changed(self, new_text: str) -> str:
        return f"Windows text field updated to: '{new_text}'"