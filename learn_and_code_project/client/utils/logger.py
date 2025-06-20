import logging
import sys
from typing import Optional

def get_logger(name: str) -> logging.Logger:
    return setup_logger(name)

def setup_logger(name: str = "news_aggregator_client_side", level: int = logging.INFO, format_string: Optional[str] = None) -> logging.Logger:    
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()