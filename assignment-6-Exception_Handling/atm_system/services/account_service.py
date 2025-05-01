from exceptions.atm_exceptions import InsufficientFundsException, DailyLimitExceededException
from utils.validators import Validators
from config.settings import Settings

class AccountService:
    def __init__(self):
        self.daily_limit = Settings.DAILY_WITHDRAWAL_LIMIT
    
    def check_balance(self, account):
        return account.balance
    
    def validate_withdrawal(self, account, amount):
        daily_withdrawals = account.get_daily_withdrawals()
        if not Validators.validate_daily_limit(daily_withdrawals, amount):
            raise DailyLimitExceededException(f"Daily withdrawal limit exceeded. Limit: {self.daily_limit}, "f"Already withdrawn: {daily_withdrawals}, Requested: {amount}")
        
        if account.balance < amount:
            raise InsufficientFundsException(f"Insufficient funds. Balance: {account.balance}, Requested: {amount}")
        
        daily_withdrawals = account.get_daily_withdrawals()
        if not Validators.validate_daily_limit(daily_withdrawals, amount):
            raise DailyLimitExceededException(f"Daily withdrawal limit exceeded. Limit: {self.daily_limit}, "f"Already withdrawn: {daily_withdrawals}, Requested: {amount}")
        
        return True
