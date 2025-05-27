from core.interfaces import (
    UIFactory,
    Button,
    Checkbox,
    TextField
)
from exceptions import ComponentCreationError
from implementations.windows.windows_button import WindowsButton
from implementations.windows.windows_checkbox import WindowsCheckbox
from implementations.windows.windows_text_field import WindowsTextField

class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        try:
            return WindowsButton()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create Windows button: {e}")
    
    def create_checkbox(self) -> Checkbox:
        try:
            return WindowsCheckbox()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create Windows checkbox: {e}")
    
    def create_text_field(self) -> TextField:
        try:
            return WindowsTextField()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create Windows text field: {e}")