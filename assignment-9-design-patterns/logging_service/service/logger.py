import inspect
import os
import threading
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Union
from core.log_entry import LogEntry
from core.log_level import LogLevel
from core.logger_config import LoggerConfig
from exceptions.logging_exceptions import LoggingException
from formatters.base_formatter import BaseFormatter
from formatters.json_formatter import JsonFormatter
from formatters.simple_formatter import SimpleFormatter
from handlers.base_handler import BaseHandler
from handlers.console_handler import ConsoleHandler
from handlers.database_handler import DatabaseHandler
from handlers.file_handler import FileHandler
from core.log_level import get_level_from_string

class Logger:
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls, name: str = "root", config: Optional[LoggerConfig] = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, name: str = "root", config: Optional[LoggerConfig] = None):
        with self._lock:
            if self._initialized:
                return
                
            self.name = name
            self._handlers: List[BaseHandler] = []
            self._child_loggers: Dict[str, 'Logger'] = {}
            self._level = LogLevel.INFO
            self._config = config or LoggerConfig.default_config()
            self._level = self._config.default_level
            self._formatters: Dict[str, BaseFormatter] = {
                'simple': SimpleFormatter(),
                'json': JsonFormatter()
            }
            self._setup_handlers()
            self._initialized = True
    
    def _setup_handlers(self) -> None:
        handlers_map = {
            'console': self._create_console_handler,
            'file': self._create_file_handler,
            'database': self._create_database_handler
        }
        
        for handler_name in self._config.enabled_handlers:
            if handler_name in self._config.handlers:
                handler_config = self._config.handlers[handler_name]
                creator_func = handlers_map.get(handler_config.handler_type)
                
                if creator_func:
                    try:
                        handler = creator_func(handler_config)
                        self._handlers.append(handler)
                    except Exception as e:
                        print(f"Error creating handler '{handler_name}': {e}")
    
    def _create_console_handler(self, config):
        formatter = self._get_formatter(config.formatter)
        use_stderr = config.params.get('use_stderr_for_errors', 'true').lower() == 'true'
        return ConsoleHandler(formatter, config.level, use_stderr)
    
    def _create_file_handler(self, config):
        formatter = self._get_formatter(config.formatter)
        filename = config.params.get('filename')
        directory = config.params.get('directory', 'logs')
        max_size_mb = int(config.params.get('max_size_mb', '0')) or None
        backup_count = int(config.params.get('backup_count', '5'))
        return FileHandler(
            formatter, config.level, filename, directory, max_size_mb, backup_count
        )
    
    def _create_database_handler(self, config):
        formatter = self._get_formatter(config.formatter)
        db_path = config.params.get('db_path', 'logs/logging.db')
        table_name = config.params.get('table_name', 'log_entries')
        return DatabaseHandler(formatter, config.level, db_path, table_name)
    
    def _get_formatter(self, formatter_name: str) -> BaseFormatter:
        return self._formatters.get(formatter_name, self._formatters['simple'])
    
    def get_child_logger(self, name: str) -> 'Logger':
        with self._lock:
            if name not in self._child_loggers:
                child = Logger()
                child.name = f"{self.name}.{name}"
                child._handlers = self._handlers
                child._level = self._level
                child._config = self._config
                child._formatters = self._formatters
                self._child_loggers[name] = child
            return self._child_loggers[name]
    
    def set_level(self, level: Union[LogLevel, str]) -> None:
        with self._lock:
            if isinstance(level, str):
                self._level = get_level_from_string(level)
            else:
                self._level = level
    
    def get_level(self) -> LogLevel:
        return self._level
    
    def _log(self, level: LogLevel, message: str, *args, exc_info: bool = False, stack_info: bool = False, extra: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        if level.value < self._level.value:
            return
            
        if args:
            try:
                message = message % args
            except Exception as e:
                message = f"{message} (Error formatting message: {e})"
        
        frame = inspect.currentframe()
        caller_frame = frame.f_back.f_back if frame and frame.f_back else None
        
        module = None
        function = None
        line_number = None
        
        if caller_frame:
            module = inspect.getmodule(caller_frame).__name__ if inspect.getmodule(caller_frame) else "<unknown>"
            function = caller_frame.f_code.co_name
            line_number = caller_frame.f_lineno
            
        exception_info = None
        if exc_info:
            exception_info = traceback.format_exc()
        
        context = {}
        if extra:
            context.update(extra)
        if kwargs:
            context.update(kwargs)
        
        log_entry = LogEntry(
            level=level,
            message=message,
            logger_name=self.name,
            thread_name=threading.current_thread().name,
            process_id=os.getpid(),
            module=module,
            function=function,
            line_number=line_number,
            exception_info=exception_info,
            context=context
        )
        
        for handler in self._handlers:
            try:
                handler.handle(log_entry)
            except Exception as e:
                print(f"Error in handler: {e}")
    
    def trace(self, message: str, *args, **kwargs) -> None:
        self._log(LogLevel.TRACE, message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        self._log(LogLevel.DEBUG, message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        self._log(LogLevel.INFO, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        self._log(LogLevel.WARNING, message, *args, **kwargs)
    
    def error(self, message: str, *args, exc_info: bool = False, **kwargs) -> None:
        self._log(LogLevel.ERROR, message, *args, exc_info=exc_info, **kwargs)
    
    def critical(self, message: str, *args, exc_info: bool = False, **kwargs) -> None:
        self._log(LogLevel.CRITICAL, message, *args, exc_info=exc_info, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        self._log(LogLevel.ERROR, message, *args, exc_info=True, **kwargs)
    
    def log(self, level: Union[LogLevel, int, str], message: str, *args, **kwargs) -> None:
        if isinstance(level, int):
            for log_level in LogLevel:
                if log_level.value == level:
                    level = log_level
                    break
            else:
                level = LogLevel.INFO
        elif isinstance(level, str):
            try:
                level = get_level_from_string(level)
            except ValueError:
                level = LogLevel.INFO
                
        self._log(level, message, *args, **kwargs)
    
    def shutdown(self) -> None:
        with self._lock:
            for handler in self._handlers:
                try:
                    handler.close()
                except Exception as e:
                    print(f"Error closing handler: {e}")
            
            for child in self._child_loggers.values():
                child._handlers = []