from typing import List, Optional
from core.platforms import Platform
from core.interfaces import Button, Checkbox, TextField
from core.factory_creator import UIFactoryCreator
from exceptions import UnsupportedPlatformError, ComponentCreationError

class Application:
    def __init__(self, platform: Platform = Platform.WINDOWS):
        try:
            self.factory = UIFactoryCreator.create_factory(platform)
            self.button: Optional[Button] = None
            self.checkbox: Optional[Checkbox] = None
            self.text_field: Optional[TextField] = None
        except UnsupportedPlatformError as e:
            print(f"Error initializing application: {e}")
            raise
    
    def create_ui(self) -> None:
        try:
            self.button = self.factory.create_button()
            self.checkbox = self.factory.create_checkbox()
            self.text_field = self.factory.create_text_field()
        except ComponentCreationError as e:
            print(f"Error creating UI components: {e}")
            raise
    
    def render_ui(self) -> List[str]:
        results = []
        
        if self.button:
            results.append(self.button.render())
        
        if self.checkbox:
            results.append(self.checkbox.render())
        
        if self.text_field:
            results.append(self.text_field.render())
        
        return results
    
    def interact_with_ui(self) -> List[str]:
        results = []
        
        if self.button:
            results.append(self.button.on_click())
        
        if self.checkbox:
            results.append(self.checkbox.toggle())
        
        if self.text_field:
            self.text_field.text = "Hello, World!"
            results.append(f"Current text: {self.text_field.text}")
        
        return results