from datetime import datetime
from config.settings import Settings

class Validators:
    @staticmethod
    def validate_daily_limit(current_withdrawals, requested_amount):
        daily_limit = Settings.DAILY_WITHDRAWAL_LIMIT
        return (current_withdrawals + requested_amount) <= daily_limit