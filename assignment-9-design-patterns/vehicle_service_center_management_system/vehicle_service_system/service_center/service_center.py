import logging
from typing import Dict, List, Any
from datetime import datetime
from constants.constants import SERVICE_CENTER_CONSTANTS as SCC
from models.vehicle import Vehicle
from factories.vehicle_factory import VehicleFactory
from exceptions.service_exceptions import (
    UnsupportedVehicleTypeError, 
    ServiceNotAvailableError,
    VehicleNotFoundError,
    ServiceCenterFullError,
    OutsideOperatingHoursError
)

logger = logging.getLogger("VehicleServiceSystem")

class ServiceCenter:    
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.vehicle_factory = VehicleFactory()
        self.serviced_vehicles: Dict[str, Vehicle] = {}
        logger.info(f"Service Center '{name}' at {location} is now operational")
    
    def _check_operating_hours(self) -> bool:
        current_hour = datetime.now().hour
        return (current_hour >= SCC.OPERATION_START_HOUR and 
                current_hour < SCC.OPERATION_END_HOUR)
    
    def _check_capacity(self) -> bool:
        return len(self.serviced_vehicles) < SCC.MAX_VEHICLES_PER_CENTER
    
    def register_vehicle(self, vehicle_type: str, registration_number: str, owner_name: str) -> Vehicle:
        if not self._check_capacity():
            logger.warning(f"Service center {self.name} is at capacity")
            raise ServiceCenterFullError(f"Service center {self.name} is at capacity")
            
        try:
            vehicle = self.vehicle_factory.create_vehicle(vehicle_type, registration_number, owner_name)
            
            self.serviced_vehicles[registration_number] = vehicle
            logger.info(f"Registered {vehicle_type} with registration {registration_number} for {owner_name}")
            
            return vehicle
            
        except UnsupportedVehicleTypeError as e:
            logger.error(f"Failed to register vehicle: {str(e)}")
            raise
    
    def get_vehicle(self, registration_number: str) -> Vehicle:
        if registration_number not in self.serviced_vehicles:
            logger.warning(f"Vehicle with registration {registration_number} not found")
            raise VehicleNotFoundError(f"Vehicle with registration {registration_number} is not registered")
        
        return self.serviced_vehicles[registration_number]
    
    def service_vehicle(self, registration_number: str, service_name: str) -> str:
        if not self._check_operating_hours():
            current_hour = datetime.now().hour
            logger.warning(f"Service requested outside operating hours (current hour: {current_hour})")
            raise OutsideOperatingHoursError(
                f"Service center is closed. Operating hours are from "
                f"{SCC.OPERATION_START_HOUR}:00 to {SCC.OPERATION_END_HOUR}:00"
            )
            
        try:
            vehicle = self.get_vehicle(registration_number)
            
            result = vehicle.request_service(service_name)
            logger.info(f"Serviced {vehicle.get_vehicle_type()} {registration_number} with {service_name}")
            
            return result
            
        except (VehicleNotFoundError, ServiceNotAvailableError) as e:
            logger.error(f"Service request failed: {str(e)}")
            raise
    
    def get_vehicle_service_history(self, registration_number: str) -> List[Dict[str, Any]]:
        vehicle = self.get_vehicle(registration_number)
        return vehicle.get_service_history()