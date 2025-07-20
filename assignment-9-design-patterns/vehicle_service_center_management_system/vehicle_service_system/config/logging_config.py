import logging
from constants.constants import LOG_CONSTANTS

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_CONSTANTS.DEFAULT_LOG_LEVEL),
        format=LOG_CONSTANTS.LOG_FORMAT,
        handlers=[logging.StreamHandler()]
    )
    
    logger = logging.getLogger(LOG_CONSTANTS.DEFAULT_LOGGER_NAME)
    return logger