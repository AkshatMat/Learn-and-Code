from models.atm import ATM
from models.card import Card
from models.account import Account
from services.auth_service import AuthService
from services.account_service import AccountService
from services.atm_service import ATMService
from services.transaction_service import TransactionService
from exceptions.atm_exceptions import ATMException

def main():
    auth_service = AuthService()
    account_service = AccountService()
    atm_service = ATMService()
    transaction_service = TransactionService(auth_service, account_service, atm_service)
    
    atm = ATM(atm_id="ATM001", cash_available=5000.0)
    account = Account(account_id="ACC123", balance=1500.0)
    card = Card(card_number="1234-5678-9012-3456", account_id="ACC123", pin="1234")
    
    print("\n~~~~~~~ Scenario 1: Successful Withdrawal ~~~~~~~")
    result = transaction_service.withdraw(atm, card, account, "1234", 500.0)
    print(result)
    
    print("\n~~~~~~~ Scenario 2: Insufficient Funds ~~~~~~~")
    result = transaction_service.withdraw(atm, card, account, "1234", 2000.0)
    print(result)
    
    print("\n~~~~~~~ Scenario 3: Insufficient Cash in ATM ~~~~~~~")
    atm.cash_available = 300.0
    result = transaction_service.withdraw(atm, card, account, "1234", 400.0)
    print(result)
    atm.cash_available = 5000.0  
    
    print("\n~~~~~~~ Scenario 5: Invalid PIN Attempts ~~~~~~~")
    for i in range(4): 
        result = transaction_service.withdraw(atm, card, account, "wrong_pin", 100.0)
        print(f"Attempt {i+1}: {result}")
        if card.is_blocked:
            break
    
    card = Card(card_number="1234-5678-9012-3456", account_id="ACC123", pin="1234")
    
    print("\n~~~~~~~ Scenario 6: Daily Limit Exceeded ~~~~~~~")
    account.daily_withdrawals = 700.0  
    result = transaction_service.withdraw(atm, card, account, "1234", 25000.0)  
    print(result)

if __name__ == "__main__":
    main()