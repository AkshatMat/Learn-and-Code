import uuid
from models.transaction import Transaction
from exceptions.atm_exceptions import InsufficientFundsException, InsufficientCashInATMException, ConnectionException, CardBlockedException, InvalidPINException, DailyLimitExceededException

class TransactionService:
    def __init__(self, auth_service, account_service, atm_service):
        self.auth_service = auth_service
        self.account_service = account_service
        self.atm_service = atm_service
        self.transactions = []
    
    def withdraw(self, atm, card, account, pin, amount):
        transaction = Transaction(transaction_id=str(uuid.uuid4()), account_id=account.account_id, amount=amount, transaction_type="WITHDRAWAL")
        try:
            self.atm_service.check_connection(atm)
            self.auth_service.authenticate(card, pin)
            self.account_service.validate_withdrawal(account, amount)
            self.atm_service.check_atm_cash(atm, amount)
            account.withdraw(amount)
            atm.dispense_cash(amount)
            
            transaction.complete()
            self.transactions.append(transaction)
            
            return {"success": True, "message": f"Successfully withdrew {amount}", "transaction_id": transaction.transaction_id, "remaining_balance": account.balance}
            
        except (InsufficientFundsException, InsufficientCashInATMException, ConnectionException, CardBlockedException, InvalidPINException, DailyLimitExceededException) as e:
            transaction.fail()
            self.transactions.append(transaction)
            return {"success": False, "message": str(e), "transaction_id": transaction.transaction_id}