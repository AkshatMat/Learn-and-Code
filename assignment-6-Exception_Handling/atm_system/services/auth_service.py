from exceptions.atm_exceptions import InvalidPINException, CardBlockedException
from config.settings import Settings

class AuthService:
    def __init__(self):
        self.max_pin_attempts = Settings.MAX_PIN_ATTEMPTS
    
    def authenticate(self, card, pin):
        if card.is_blocked:
            raise CardBlockedException("Card is blocked due to too many invalid PIN attempts")
        
        if not card.validate_pin(pin):
            if card.is_pin_attempts_exceeded(self.max_pin_attempts):
                card.block_card()
                raise CardBlockedException(f"Card has been blocked after {self.max_pin_attempts} invalid attempts")
            remaining_attempts = self.max_pin_attempts - card.pin_attempts
            raise InvalidPINException(f"Invalid PIN. {remaining_attempts} attempts remaining")
        
        return True