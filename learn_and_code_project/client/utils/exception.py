class NewsAggregatorException(Exception):
    pass

class ConfigurationError(NewsAggregatorException):
    pass

class NewsAPIError(NewsAggregatorException):
    pass

class ScrapingError(NewsAggregatorException):
    pass

class DatabaseError(NewsAggregatorException):
    pass

class ValidationError(NewsAggregatorException):
    pass

class KeywordExtractionError(NewsAggregatorException):
    pass

class RepositoryError(NewsAggregatorException):
    pass