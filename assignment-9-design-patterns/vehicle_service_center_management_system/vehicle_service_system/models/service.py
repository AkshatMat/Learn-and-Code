from abc import ABC, abstractmethod
from constants.constants import SERVICE_CONSTANTS as SC

class Service(ABC):    
    @abstractmethod
    def perform_service(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

class CarOilChangeService(Service):
    def perform_service(self) -> str:
        return "Changed car oil with premium synthetic oil"
    
    def get_description(self) -> str:
        return "Full oil change service including filter replacement"
    
    def get_cost(self) -> float:
        return SC.CAR_OIL_CHANGE_COST

class CarBrakeInspectionService(Service):
    def perform_service(self) -> str:
        return "Inspected and adjusted car brakes"
    
    def get_description(self) -> str:
        return "Complete brake system inspection and adjustment"
    
    def get_cost(self) -> float:
        return SC.CAR_BRAKE_INSPECTION_COST

class CarTireRotationService(Service):
    def perform_service(self) -> str:
        return "Rotated and balanced all car tires"
    
    def get_description(self) -> str:
        return "Tire rotation and balancing service"
    
    def get_cost(self) -> float:
        return SC.CAR_TIRE_ROTATION_COST

class BikeChainLubricationService(Service):    
    def perform_service(self) -> str:
        return "Lubricated bike chain for smooth operation"
    
    def get_description(self) -> str:
        return "Chain cleaning and lubrication service"
    
    def get_cost(self) -> float:
        return SC.BIKE_CHAIN_LUBRICATION_COST


class BikeBrakeTighteningService(Service):
    def perform_service(self) -> str:
        return "Tightened and adjusted bike brakes"
    
    def get_description(self) -> str:
        return "Brake adjustment and tightening service"
    
    def get_cost(self) -> float:
        return SC.BIKE_BRAKE_TIGHTENING_COST

class TruckEngineDiagnosticsService(Service):
    def perform_service(self) -> str:
        return "Performed heavy-duty engine diagnostics on truck"
    
    def get_description(self) -> str:
        return "Comprehensive engine diagnostic service for heavy-duty trucks"
    
    def get_cost(self) -> float:
        return SC.TRUCK_ENGINE_DIAGNOSTICS_COST

class TruckCargoInspectionService(Service):
    def perform_service(self) -> str:
        return "Inspected truck cargo area and securing mechanisms"
    
    def get_description(self) -> str:
        return "Complete cargo area and tie-down inspection"
    
    def get_cost(self) -> float:
        return SC.TRUCK_CARGO_INSPECTION_COST
