class ATM:
    def __init__(self, atm_id, cash_available=10000.0):
        self.atm_id = atm_id
        self.cash_available = cash_available
        self.is_connected = True
    
    def has_sufficient_cash(self, amount):
        return self.cash_available >= amount
    
    def dispense_cash(self, amount):
        if self.has_sufficient_cash(amount):
            self.cash_available -= amount
            return True
        
        return False
    
    def is_server_connected(self):
        return self.is_connected
    