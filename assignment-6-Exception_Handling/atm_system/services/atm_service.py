from exceptions.atm_exceptions import InsufficientCashInATMException, ConnectionException

class ATMService:
    def check_atm_cash(self, atm, amount):
        if not atm.has_sufficient_cash(amount):
            raise InsufficientCashInATMException(f"ATM has insufficient cash. Available: {atm.cash_available}, Requested: {amount}")
        return True
    
    def check_connection(self, atm):
        if not atm.is_server_connected():
            raise ConnectionException("Unable to connect to server")
        return True
