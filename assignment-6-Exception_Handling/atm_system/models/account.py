from datetime import datetime

class Account:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.daily_withdrawals = 0.0
        self.last_withdrawal_date = None
        
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        
        today = datetime.now().date()
        if self.last_withdrawal_date != today:
            self.daily_withdrawals = 0.0
            self.last_withdrawal_date = today
            
        self.balance -= amount
        self.daily_withdrawals += amount
        self.last_withdrawal_date = today

        return True
    
    def get_daily_withdrawals(self):
        today = datetime.now().date()
        if self.last_withdrawal_date != today:
            self.daily_withdrawals = 0.0
            self.last_withdrawal_date = today
            
        return self.daily_withdrawals