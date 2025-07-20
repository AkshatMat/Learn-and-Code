from core.log_entry import LogEntry
from formatters.base_formatter import BaseFormatter

class SimpleFormatter(BaseFormatter):
    def format(self, log_entry: LogEntry) -> str:
        timestamp = log_entry.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        base_msg = f"[{timestamp}] [{log_entry.level}] [{log_entry.logger_name}] - {log_entry.message}"

        source_info = []
        if log_entry.module:
            source_info.append(f"module={log_entry.module}")
        if log_entry.function:
            source_info.append(f"function={log_entry.function}")
        if log_entry.line_number:
            source_info.append(f"line={log_entry.line_number}")
            
        if source_info:
            base_msg += f" ({', '.join(source_info)})"
            
        if log_entry.exception_info:
            base_msg += f"\nException: {log_entry.exception_info}"
            
        if log_entry.context:
            context_str = ", ".join(f"{k}={v}" for k, v in log_entry.context.items())
            base_msg += f"\nContext: {{{context_str}}}"
            
        return base_msg