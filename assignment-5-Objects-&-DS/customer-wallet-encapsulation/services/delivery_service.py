from interfaces.payment import PaymentProcessor

class DeliveryService:    
    def collect_payment(self, payment_processor: PaymentProcessor, amount: float) -> bool:
        try:
            if amount <= 0:
                raise ValueError("Payment amount must be positive")
            
            if payment_processor.process_payment(amount):
                print(f"Payment of ${amount:.2f} received!")
                return True
            else:
                print("Insufficient funds. Will come back later.")
                return False
                
        except ValueError as e:
            print(f"Error: {e}")
            return False