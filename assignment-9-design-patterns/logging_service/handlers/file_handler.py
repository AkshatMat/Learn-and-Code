import os
from datetime import datetime
from typing import Optional
from core.log_entry import LogEntry
from core.log_level import LogLevel
from exceptions.logging_exceptions import HandlerException
from formatters.base_formatter import BaseFormatter
from handlers.base_handler import BaseHandler

class FileHandler(BaseHandler):
    def __init__(self, formatter: BaseFormatter, level: LogLevel = LogLevel.INFO, filename: str = None, directory: str = 'logs', max_size_mb: Optional[int] = None, backup_count: int = 5):
        super().__init__(formatter, level)
        
        self.directory = directory
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                raise HandlerException(f"Unable to create log directory: {e}")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"application_{timestamp}.log"
            
        self.filename = os.path.join(directory, filename)
        self.max_size_bytes = max_size_mb * 1024 * 1024 if max_size_mb else None
        self.backup_count = backup_count
        self.file = None
        
        try:
            self.file = open(self.filename, 'a', encoding='utf-8')
        except IOError as e:
            raise HandlerException(f"Unable to open log file: {e}")
    
    def _emit(self, log_entry: LogEntry, formatted_entry: str) -> None:
        if self.file is None:
            try:
                self.file = open(self.filename, 'a', encoding='utf-8')
            except IOError as e:
                print(f"Error reopening log file: {e}")
                return
                
        try:
            self.file.write(formatted_entry + "\n")
            self.file.flush()
            
            if self.max_size_bytes and self._should_rotate():
                self._rotate_log()
                
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def _should_rotate(self) -> bool:
        try:
            return os.path.getsize(self.filename) >= self.max_size_bytes
        except OSError:
            return False
    
    def _rotate_log(self) -> None:
        if self.file:
            self.file.close()
            self.file = None
            
        oldest_backup = f"{self.filename}.{self.backup_count}"
        if os.path.exists(oldest_backup):
            try:
                os.remove(oldest_backup)
            except OSError:
                pass
                
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.filename}.{i}"
            dst = f"{self.filename}.{i + 1}"
            if os.path.exists(src):
                try:
                    os.rename(src, dst)
                except OSError:
                    pass
                    
        if os.path.exists(self.filename):
            try:
                os.rename(self.filename, f"{self.filename}.1")
            except OSError as e:
                print(f"Error rotating log file: {e}")
                
        try:
            self.file = open(self.filename, 'a', encoding='utf-8')
        except IOError as e:
            print(f"Error creating new log file after rotation: {e}")
    
    def close(self) -> None:
        if self.file:
            self.file.close()
            self.file = None