import json
from core.log_entry import LogEntry
from formatters.base_formatter import BaseFormatter

class JsonFormatter(BaseFormatter):
    def format(self, log_entry: LogEntry) -> str:
        return json.dumps(log_entry.to_dict())