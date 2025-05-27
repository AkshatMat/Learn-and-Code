from abc import ABC, abstractmethod
from core.log_entry import LogEntry
from core.log_level import LogLevel
from exceptions.logging_exceptions import HandlerException
from formatters.base_formatter import BaseFormatter

class BaseHandler(ABC):
    def __init__(self, formatter: BaseFormatter, level: LogLevel = LogLevel.INFO):
        self.formatter = formatter
        self.level = level
        
    def handle(self, log_entry: LogEntry) -> None:
        if log_entry.level.value >= self.level.value:
            try:
                formatted_entry = self.formatter.format(log_entry)
                self._emit(log_entry, formatted_entry)
            except Exception as e:
                print(f"Error in log handler: {str(e)}")
    
    @abstractmethod
    def _emit(self, log_entry: LogEntry, formatted_entry: str) -> None:
        pass
    
    def close(self) -> None:
        pass