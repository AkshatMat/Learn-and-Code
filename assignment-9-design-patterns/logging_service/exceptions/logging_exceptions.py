class LoggingException(Exception):
    pass

class ConfigurationException(LoggingException):
    pass

class HandlerException(LoggingException):
    pass

class FormatterException(LoggingException):
    pass