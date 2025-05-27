class SERVICE_CENTER_CONSTANTS:
    DEFAULT_CENTER_NAME = "City Service Center"
    DEFAULT_CENTER_LOCATION = "123 Main St"

    MAX_VEHICLES_PER_CENTER = 1000
    OPERATION_START_HOUR = 8
    OPERATION_END_HOUR = 18

class VEHICLE_CONSTANTS:
    CAR_TYPE = "car"
    BIKE_TYPE = "bike" 
    TRUCK_TYPE = "truck"
    
    CAR_DISPLAY_NAME = "Car"
    BIKE_DISPLAY_NAME = "Bike"
    TRUCK_DISPLAY_NAME = "Truck"

    MIN_REGISTRATION_LENGTH = 3
    MAX_REGISTRATION_LENGTH = 10

class SERVICE_CONSTANTS:
    CAR_OIL_CHANGE = "oil_change"
    CAR_BRAKE_INSPECTION = "brake_inspection"
    CAR_TIRE_ROTATION = "tire_rotation"
    
    BIKE_CHAIN_LUBRICATION = "chain_lubrication"
    BIKE_BRAKE_TIGHTENING = "brake_tightening"
    
    TRUCK_ENGINE_DIAGNOSTICS = "engine_diagnostics"
    TRUCK_CARGO_INSPECTION = "cargo_inspection"
    
    CAR_OIL_CHANGE_COST = 100.00
    CAR_BRAKE_INSPECTION_COST = 100.00
    CAR_TIRE_ROTATION_COST = 1500.00
    
    BIKE_CHAIN_LUBRICATION_COST = 100.00
    BIKE_BRAKE_TIGHTENING_COST = 100.00
    
    TRUCK_ENGINE_DIAGNOSTICS_COST = 1500.00
    TRUCK_CARGO_INSPECTION_COST = 2000.00

class LOG_CONSTANTS:
    DEFAULT_LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEFAULT_LOGGER_NAME = "VehicleServiceSystem"