"""
Vehicle interface and implementations for Vehicle Service Center Management System
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

from constants.constants import VEHICLE_CONSTANTS as VC
from constants.constants import SERVICE_CONSTANTS as SC
from models.service import (
    Service, 
    CarOilChangeService, CarBrakeInspectionService, CarTireRotationService,
    BikeChainLubricationService, BikeBrakeTighteningService,
    TruckEngineDiagnosticsService, TruckCargoInspectionService
)
from exceptions.service_exceptions import ServiceNotAvailableError, InvalidRegistrationError

logger = logging.getLogger("VehicleServiceSystem")

class Vehicle(ABC):
    def __init__(self, registration_number: str, owner_name: str):
        if (len(registration_number) < VC.MIN_REGISTRATION_LENGTH or 
            len(registration_number) > VC.MAX_REGISTRATION_LENGTH):
            raise InvalidRegistrationError(
                f"Registration number must be between {VC.MIN_REGISTRATION_LENGTH} and "
                f"{VC.MAX_REGISTRATION_LENGTH} characters"
            )
            
        self.registration_number = registration_number
        self.owner_name = owner_name
        self.service_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def get_vehicle_type(self) -> str:
        pass
    
    @abstractmethod
    def get_available_services(self) -> Dict[str, Service]:
        pass
    
    def request_service(self, service_name: str) -> str:
        available_services = self.get_available_services()
        
        if service_name not in available_services:
            available_service_names = ", ".join(available_services.keys())
            raise ServiceNotAvailableError(
                f"Service '{service_name}' is not available for {self.get_vehicle_type()}. "
                f"Available services: {available_service_names}"
            )
        
        service = available_services[service_name]
        result = service.perform_service()
        
        self.service_history.append({
            "service_name": service_name,
            "date": datetime.now(),
            "cost": service.get_cost()
        })
        
        return result
    
    def get_service_history(self) -> List[Dict[str, Any]]:
        return self.service_history

class Car(Vehicle):
    def get_vehicle_type(self) -> str:
        return VC.CAR_DISPLAY_NAME
    
    def get_available_services(self) -> Dict[str, Service]:
        return {
            SC.CAR_OIL_CHANGE: CarOilChangeService(),
            SC.CAR_BRAKE_INSPECTION: CarBrakeInspectionService(),
            SC.CAR_TIRE_ROTATION: CarTireRotationService()
        }

class Bike(Vehicle):
    def get_vehicle_type(self) -> str:
        return VC.BIKE_DISPLAY_NAME
    
    def get_available_services(self) -> Dict[str, Service]:
        return {
            SC.BIKE_CHAIN_LUBRICATION: BikeChainLubricationService(),
            SC.BIKE_BRAKE_TIGHTENING: BikeBrakeTighteningService()
        }

class Truck(Vehicle):
    def get_vehicle_type(self) -> str:
        return VC.TRUCK_DISPLAY_NAME
    
    def get_available_services(self) -> Dict[str, Service]:
        return {
            SC.TRUCK_ENGINE_DIAGNOSTICS: TruckEngineDiagnosticsService(),
            SC.TRUCK_CARGO_INSPECTION: TruckCargoInspectionService()
        }