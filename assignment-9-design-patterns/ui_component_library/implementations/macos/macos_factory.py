from core.interfaces import (
    UIFactory,
    Button,
    Checkbox,
    TextField
)
from exceptions import ComponentCreationError
from implementations.macos.macos_button import MacOSButton
from implementations.macos.macos_checkbox import MacOSCheckbox
from implementations.macos.macos_text_field import MacOSTextField

class MacOSUIFactory(UIFactory):    
    def create_button(self) -> Button:
        try:
            return MacOSButton()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create MacOS button: {e}")
    
    def create_checkbox(self) -> Checkbox:
        try:
            return MacOSCheckbox()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create MacOS checkbox: {e}")
    
    def create_text_field(self) -> TextField:
        try:
            return MacOSTextField()
        except Exception as e:
            raise ComponentCreationError(f"Failed to create MacOS text field: {e}")