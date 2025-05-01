from abc import ABC, abstractmethod
from .exceptions import LocationNotFoundError, GeocodeServiceError
from .locations import Location

class GeocoderInterface(ABC):
    @abstractmethod
    def geocode(self, location_name):
        pass

class NominatimGeocoder(GeocoderInterface):
    def __init__(self, user_agent="geoapp"):
        try:
            from geopy.geocoders import Nominatim
            self.geolocator = Nominatim(user_agent=user_agent)
        except ImportError:
            raise ImportError("geopy package is required. Install it using 'pip install geopy'")
    
    def geocode(self, location_name):
        try:
            geocode_result = self.geolocator.geocode(location_name)
            
            if geocode_result:
                return Location(name=location_name, latitude=geocode_result.latitude, longitude=geocode_result.longitude)
            else:
                raise LocationNotFoundError(f"Could not find coordinates for location: {location_name}")
        except Exception as e:
            if isinstance(e, LocationNotFoundError):
                raise
            raise GeocodeServiceError(f"Error geocoding location '{location_name}': {str(e)}")