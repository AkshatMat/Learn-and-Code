from core.interfaces import TextField

class MacOSTextField(TextField):
    def render(self) -> str:
        return f"Rendering a MacOS-style text field with text: '{self._text}'"
    
    def on_text_changed(self, new_text: str) -> str:
        return f"MacOS text field updated to: '{new_text}'"