class NewsAggregatorException(Exception):
    pass

class AuthenticationError(NewsAggregatorException):
    pass

class AuthorizationError(NewsAggregatorException):
    pass

class ValidationError(NewsAggregatorException):
    pass

class DatabaseError(NewsAggregatorException):
    pass

class UserNotFoundError(NewsAggregatorException):
    pass

class ArticleNotFoundError(NewsAggregatorException):
    pass

class PasswordError(NewsAggregatorException):
    pass

class JWTError(NewsAggregatorException):
    pass

class ConnectionError(NewsAggregatorException):
    pass

class APIError(NewsAggregatorException):
    pass

class NotificationError(NewsAggregatorException):
    pass

class EmailError(NewsAggregatorException):
    pass

class ServiceError(NewsAggregatorException):
    pass

class ManagerError(NewsAggregatorException):
    pass
