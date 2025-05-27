import logging
from .exceptions import GeocodingError
from .geocoder import NominatimGeocoder

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_location_coordinates(location_name, geocoder=None):
    if geocoder is None:
        geocoder = NominatimGeocoder()
    try:
        location = geocoder.geocode(location_name)
        return location.latitude, location.longitude
    except GeocodingError as e:
        logger.error(str(e))
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None, None

if __name__ == "__main__":
    location_name = str(input())
    
    try:
        latitude, longitude = get_location_coordinates(location_name)
        
        if latitude is not None and longitude is not None:
            print(f"Coordinates for {location_name}: ({latitude}, {longitude})")
        else:
            print(f"Could not find coordinates for {location_name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")