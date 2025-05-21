import sqlite3
from typing import Dict, Optional
from core.log_entry import LogEntry
from core.log_level import LogLevel
from exceptions.logging_exceptions import HandlerException
from formatters.base_formatter import BaseFormatter
from handlers.base_handler import BaseHandler

class DatabaseHandler(BaseHandler):
    def __init__(self, formatter: BaseFormatter, level: LogLevel = LogLevel.INFO, db_path: str = "logs/logging.db", table_name: str = "log_entries"):
        super().__init__(formatter, level)
        self.db_path = db_path
        self.table_name = table_name
        self.connection = None
        
        try:
            self._initialize_db()
        except Exception as e:
            raise HandlerException(f"Failed to initialize database: {e}")
    
    def _initialize_db(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    logger_name TEXT,
                    message TEXT NOT NULL,
                    thread_name TEXT,
                    process_id INTEGER,
                    module TEXT,
                    function TEXT,
                    line_number INTEGER,
                    exception_info TEXT,
                    context TEXT
                )
            ''')
            
            self.connection.commit()
            
        except sqlite3.Error as e:
            if self.connection:
                self.connection.close()
                self.connection = None
            raise HandlerException(f"Database initialization error: {e}")
    
    def _emit(self, log_entry: LogEntry, formatted_entry: str) -> None:
        if not self.connection:
            try:
                self.connection = sqlite3.connect(self.db_path)
            except sqlite3.Error as e:
                print(f"Error connecting to database: {e}")
                return
                
        try:
            cursor = self.connection.cursor()
            context_str = str(log_entry.context) if log_entry.context else None
            
            cursor.execute(
                f'''
                INSERT INTO {self.table_name} (
                    id, timestamp, level, logger_name, message,
                    thread_name, process_id, module, function,
                    line_number, exception_info, context
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    log_entry.log_id,
                    log_entry.timestamp.isoformat(),
                    str(log_entry.level),
                    log_entry.logger_name,
                    log_entry.message,
                    log_entry.thread_name,
                    log_entry.process_id,
                    log_entry.module,
                    log_entry.function,
                    log_entry.line_number,
                    log_entry.exception_info,
                    context_str
                )
            )
            
            self.connection.commit()
            
        except sqlite3.Error as e:
            print(f"Error writing to database: {e}")
    
    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None