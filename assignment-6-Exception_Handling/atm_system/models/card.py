class Card:
    def __init__(self, card_number, account_id, pin):
        self.card_number = card_number
        self.account_id = account_id
        self.pin = pin
        self.is_blocked = False
        self.pin_attempts = 0
    
    def validate_pin(self, entered_pin):
        if self.is_blocked:
            return False
        
        if self.pin == entered_pin:
            self.pin_attempts = 0
            return True
        
        self.pin_attempts += 1
        return False
    
    def is_pin_attempts_exceeded(self, max_attempts):
        return self.pin_attempts >= max_attempts
    
    def block_card(self):
        self.is_blocked = True