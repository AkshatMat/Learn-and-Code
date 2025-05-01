class ATMException(Exception):
    pass

class InsufficientFundsException(ATMException):
    pass

class InsufficientCashInATMException(ATMException):
    pass

class ConnectionException(ATMException):
    pass

class CardBlockedException(ATMException):
    pass

class InvalidPINException(ATMException):
    pass

class DailyLimitExceededException(ATMException):
    pass