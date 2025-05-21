class ServiceSystemError(Exception):
    pass

class UnsupportedVehicleTypeError(ServiceSystemError):
    pass

class ServiceNotAvailableError(ServiceSystemError):
    pass

class InvalidRegistrationError(ServiceSystemError):
    pass

class VehicleNotFoundError(ServiceSystemError):
    pass

class ServiceCenterFullError(ServiceSystemError):
    pass

class OutsideOperatingHoursError(ServiceSystemError):
    pass