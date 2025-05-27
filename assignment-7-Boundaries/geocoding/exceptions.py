class GeocodingError(Exception):
    pass

class LocationNotFoundError(GeocodingError):
    pass

class GeocodeServiceError(GeocodingError):
    pass
