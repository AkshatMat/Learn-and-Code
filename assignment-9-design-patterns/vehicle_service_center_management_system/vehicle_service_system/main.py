import logging
from datetime import datetime
from config.logging_config import setup_logging
from exceptions.service_exceptions import ServiceSystemError, UnsupportedVehicleTypeError, ServiceNotAvailableError
from service_center.service_center import ServiceCenter
from constants.constants import SERVICE_CENTER_CONSTANTS as SCC
from constants.constants import VEHICLE_CONSTANTS as VC
from constants.constants import SERVICE_CONSTANTS as SC

logger = setup_logging()

def main():
    try:
        city_service_center = ServiceCenter(SCC.DEFAULT_CENTER_NAME, SCC.DEFAULT_CENTER_LOCATION)
        
        car = city_service_center.register_vehicle(VC.CAR_TYPE, "ABC123", "John Doe")
        bike = city_service_center.register_vehicle(VC.BIKE_TYPE, "XYZ789", "Jane Smith")
        truck = city_service_center.register_vehicle(VC.TRUCK_TYPE, "TRK456", "Bob Johnson")
        
        print(city_service_center.service_vehicle("ABC123", SC.CAR_OIL_CHANGE))
        print(city_service_center.service_vehicle("ABC123", SC.CAR_TIRE_ROTATION))
        print(city_service_center.service_vehicle("XYZ789", SC.BIKE_CHAIN_LUBRICATION))
        print(city_service_center.service_vehicle("TRK456", SC.TRUCK_ENGINE_DIAGNOSTICS))
        
        print("\nCar Service History:")
        for service in city_service_center.get_vehicle_service_history("ABC123"):
            print(f"- {service['service_name']} on {service['date']} ({service['cost']:.2f} Rupee)")
        
        print("\nTrying unavailable service:")
        try:
            city_service_center.service_vehicle("XYZ789", SC.CAR_OIL_CHANGE)
        except ServiceNotAvailableError as e:
            print(f"Error: {str(e)}")
        
        print("\nTrying unsupported vehicle type:")
        try:
            city_service_center.register_vehicle("boat", "BOAT1", "Captain Cook")
        except UnsupportedVehicleTypeError as e:
            print(f"Error: {str(e)}")

    except ServiceSystemError as e:
        print(f"Service System Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()