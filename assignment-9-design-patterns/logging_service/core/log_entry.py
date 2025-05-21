import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from core.log_level import LogLevel

@dataclass
class LogEntry:
    level: LogLevel
    message: str
    timestamp: datetime = None
    logger_name: str = ""
    thread_name: Optional[str] = None
    process_id: Optional[int] = None
    module: Optional[str] = None
    function: Optional[str] = None
    line_number: Optional[int] = None
    exception_info: Optional[str] = None
    context: Dict[str, Any] = None
    log_id: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.context is None:
            self.context = {}
        if self.log_id is None:
            self.log_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.log_id,
            'timestamp': self.timestamp.isoformat(),
            'level': str(self.level),
            'logger_name': self.logger_name,
            'message': self.message,
            'thread_name': self.thread_name,
            'process_id': self.process_id,
            'module': self.module,
            'function': self.function,
            'line_number': self.line_number,
            'exception_info': self.exception_info,
            'context': self.context
        }