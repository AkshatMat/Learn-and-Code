class PlatformError(Exception):
    pass

class UnsupportedPlatformError(PlatformError):
    pass

class ComponentCreationError(PlatformError):
    pass