import sys
from core.log_entry import LogEntry
from core.log_level import LogLevel
from formatters.base_formatter import BaseFormatter
from handlers.base_handler import BaseHandler

class ConsoleHandler(BaseHandler):
    def __init__(self, formatter: BaseFormatter, level: LogLevel = LogLevel.INFO, use_stderr_for_errors: bool = True):
        super().__init__(formatter, level)
        self.use_stderr_for_errors = use_stderr_for_errors
    
    def _emit(self, log_entry: LogEntry, formatted_entry: str) -> None:
        if self.use_stderr_for_errors and log_entry.level.value >= LogLevel.ERROR.value:
            print(formatted_entry, file=sys.stderr, flush=True)
        else:
            print(formatted_entry, flush=True)