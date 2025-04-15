from models.customer import Customer
from services.delivery_service import DeliveryService

def main():
    try:
        john = Customer("John", "Doe")
        john.receive_payment(5.0)
        
        delivery_service = DeliveryService()        
        delivery_service.collect_payment(john, 10.0)
        print(f"Remaining balance: {john.get_wallet_balance():.2f} Rupee")

        delivery_service.collect_payment(john, 10.0)
        delivery_service.collect_payment(john, -1.0)
        
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()