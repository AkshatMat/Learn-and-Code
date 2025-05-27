import os
from typing import Optional
from core.logger_config import LoggerConfig
from exceptions.logging_exceptions import ConfigurationException
from service.logger import Logger

class LoggerFactory:
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = "root") -> Logger:
        if name not in cls._loggers:
            if name == "root":
                config = cls._load_config()
                cls._loggers[name] = Logger(name, config)
            else:
                root_logger = cls.get_logger("root")
                cls._loggers[name] = root_logger.get_child_logger(name)
                
        return cls._loggers[name]
    
    @classmethod
    def _load_config(cls) -> Optional[LoggerConfig]:
        config_paths = [
            os.path.join(os.getcwd(), "logger_config.ini"),
            os.path.join(os.getcwd(), "config", "logger_config.ini"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "logger_config.ini")
        ]
        
        env_config_path = os.environ.get("LOGGER_CONFIG_PATH")
        if env_config_path:
            config_paths.insert(0, env_config_path)
            
        for path in config_paths:
            if os.path.exists(path):
                try:
                    return LoggerConfig.from_file(path)
                except ConfigurationException as e:
                    print(f"Warning: Error loading config from {path}: {e}")
        
        return LoggerConfig.default_config()
    
    @classmethod
    def shutdown_all(cls) -> None:
        for logger in cls._loggers.values():
            logger.shutdown()
        cls._loggers.clear()


get_logger = LoggerFactory.get_logger