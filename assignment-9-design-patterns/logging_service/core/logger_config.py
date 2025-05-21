import configparser
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from exceptions.logging_exceptions import ConfigurationException
from core.log_level import LogLevel, get_level_from_string

@dataclass
class HandlerConfig:
    handler_type: str
    formatter: str
    level: LogLevel
    params: Dict[str, str] = field(default_factory=dict)

@dataclass
class LoggerConfig:
    default_level: LogLevel = LogLevel.INFO
    handlers: Dict[str, HandlerConfig] = field(default_factory=dict)
    default_formatter: str = "simple"
    enabled_handlers: Set[str] = field(default_factory=set)

    @classmethod
    def from_file(cls, config_path: str) -> 'LoggerConfig':
        if not os.path.exists(config_path):
            raise ConfigurationException(f"Configuration file not found: {config_path}")

        config = configparser.ConfigParser()
        try:
            config.read(config_path)
            
            default_level_str = config.get('general', 'default_level', fallback='INFO')
            try:
                default_level = get_level_from_string(default_level_str)
            except ValueError as e:
                raise ConfigurationException(str(e))
                
            default_formatter = config.get('general', 'default_formatter', fallback='simple')
            
            handlers = {}
            enabled_handlers = set()
            
            if config.has_section('handlers'):
                enabled_handlers_str = config.get('handlers', 'enabled', fallback='console')
                enabled_handlers = {h.strip() for h in enabled_handlers_str.split(',')}
            
            for handler_name in enabled_handlers:
                section_name = f"handler:{handler_name}"
                if not config.has_section(section_name):
                    raise ConfigurationException(f"Configuration for handler '{handler_name}' not found")
                
                handler_type = config.get(section_name, 'type', fallback='console')
                formatter = config.get(section_name, 'formatter', fallback=default_formatter)
                
                level_str = config.get(section_name, 'level', fallback=default_level_str)
                try:
                    level = get_level_from_string(level_str)
                except ValueError as e:
                    raise ConfigurationException(str(e))
                
                params = {}
                for key, value in config.items(section_name):
                    if key not in ('type', 'formatter', 'level'):
                        params[key] = value
                
                handlers[handler_name] = HandlerConfig(
                    handler_type=handler_type,
                    formatter=formatter,
                    level=level,
                    params=params
                )
            
            return cls(
                default_level=default_level,
                handlers=handlers,
                default_formatter=default_formatter,
                enabled_handlers=enabled_handlers
            )
            
        except (configparser.Error, ValueError) as e:
            raise ConfigurationException(f"Error parsing configuration file: {str(e)}")
    
    @classmethod
    def default_config(cls) -> 'LoggerConfig':
        return cls(
            default_level=LogLevel.INFO,
            handlers={
                'console': HandlerConfig(
                    handler_type='console',
                    formatter='simple',
                    level=LogLevel.INFO
                )
            },
            default_formatter='simple',
            enabled_handlers={'console'}
        )