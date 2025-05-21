from core.platforms import Platform
from core.interfaces import UIFactory
from exceptions import UnsupportedPlatformError
from implementations.windows.windows_factory import WindowsUIFactory
from implementations.macos.macos_factory import MacOSUIFactory

class UIFactoryCreator:
    @staticmethod
    def create_factory(platform: Platform) -> UIFactory:
        if platform == Platform.WINDOWS:
            return WindowsUIFactory()
        elif platform == Platform.MACOS:
            return MacOSUIFactory()
        else:
            raise UnsupportedPlatformError(f"Platform {platform} is not supported.")