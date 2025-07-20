from abc import ABC, abstractmethod
from core.log_entry import LogEntry

class BaseFormatter(ABC):
    @abstractmethod
    def format(self, log_entry: LogEntry) -> str:
        pass