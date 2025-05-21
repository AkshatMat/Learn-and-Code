from datetime import datetime
import logging
from constants.constants import VEHICLE_CONSTANTS as VC
from models.vehicle import Vehicle, Car, Bike, Truck
from exceptions.service_exceptions import UnsupportedVehicleTypeError

logger = logging.getLogger("VehicleServiceSystem")

class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str, registration_number: str, owner_name: str) -> Vehicle:
        vehicle_type = vehicle_type.lower()
        
        logger.debug(
            f"Attempting to create vehicle of type {vehicle_type} "
            f"with registration {registration_number} for {owner_name}"
        )
        
        if vehicle_type == VC.CAR_TYPE:
            return Car(registration_number, owner_name)
        elif vehicle_type == VC.BIKE_TYPE:
            return Bike(registration_number, owner_name)
        elif vehicle_type == VC.TRUCK_TYPE:
            return Truck(registration_number, owner_name)
        else:
            logger.error(f"Unsupported vehicle type: {vehicle_type}")
            raise UnsupportedVehicleTypeError(f"Unsupported vehicle type: {vehicle_type}")