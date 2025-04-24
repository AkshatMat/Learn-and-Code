import time 
import logger 
from live_code.report_generation import ReportGeneration
from live_code.customer import Customer
from live_code.product import Product
from live_code.notification import NotificationService
from live_code.order_class import Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

active_orders = []
processing_queue = []
random_queue = []
pending_queue = []

class OrderProcessor:
    def __init__(self):
        self.customers = {}
        self.products = {}
        self.order_database = {}
        self.product_database = {}
        self.customer_database = {}

    def get_order(self, order_id):
        try:
            order = self.order_database.get(order_id)
            if order is None:
                raise ValueError
        except (ValueError, TypeError, NameError):
            logger.info("order_id not present in database!!!")
        else:
            return order
        
    def get_customer(self, order):
        try:
            customer = self.customers.get(order['customer_id'])
            if customer is None:
                raise ValueError
        except (ValueError, TypeError, NameError):
            logger.info("order_id not present in database!!!")
        else:
            return customer
    
    def get_product(self,item):
        try:
            product = self.products.get(item)
            if product is None:
                raise ValueError
        except (ValueError, TypeError, NameError)as e:
            logger.info("product not present in database!!!")
        else:
            return product
    
    def _is_stock_adequate(self,product,item):
        try:
            if product['stock'] > item['quantity']:
                logger.info(f"sufficient stock for product {item['product_id']}")
        except (ValueError, TypeError) as e:
            logger.info("Stock is not Adequate")
            logger.info(e)
        else:
            logger.info("Stock is Adequate!!!")
    
    def stock_reduction(self,product, item):
        try:
            product['stock'] -= item['quantity']
            if product['stock'] < 0:
                raise ValueError
        except (ValueError,TypeError):
            logger.info("Stock successfully reduced!!")
        else:
            self.products[item['product_id']] = product
    
    def stock_addition(self,product, item):
        try:
            product['stock'] += item['quantity']
            if product['stock'] < 0:
                raise ValueError
        except (ValueError,TypeError):
            logger.info("Stock successfully reduced!!")
        else:
            self.products[item['product_id']] = product
    
    def membership_level_discount(self, customer):
        try:
            discount = 0
            if customer['membership_level'] == 'gold':
                discount = 0.1
            elif customer['membership_level'] == 'platinum':
                discount = 0.15
            elif customer['membership_level'] == 'diamond':
                discount = 0.2
        except ValueError as e:
            logger.info(e)
        else:
            return discount
        
    def order_in_processing_details(self, order, discount):
        try:
            order['status'] = 'processing'
            order['discount_applied'] = order['total_amount'] * discount
            order['final_amount'] = order['total_amount'] - order['discount_applied']
            order['updated_at'] = '2024-02-10'
        except (NameError, ValueError, TypeError) as e:
            logger.info(e)
        else:
            return order
    
    def order_cancelled_details(self,order):
        try:
            order['status'] = 'cancelled'
            order['updated_at'] = '2024-02-10'
        except Exception as e:
            logger.info(e)
        
    def database_operations(self,order):
        try:
            self.order_database[order_id] = order
            active_orders.append(order)
            processing_queue.append(order_id)
        except (NameError, ValueError, TypeError) as e:
            logger.info(e)

    # make class for this
    def process_order(self, order_id):
        logger.info(f"Processing order: {order_id}")

        order = self.get_order(order_id)
        customer = self.get_customer(order)

        for item in order['items']:
            product = self.get_product(item)
            self._is_stock_adequate(product,item)

        for item in order['items']:
            product = self.get_product(item)
            self.stock_reduction(product, item)

        discount = self.membership_level_discount(customer)

        if order['total_amount'] > 1000:
            discount += 0.05

        self.order_updation(order,discount)

        self.database_operations(order)

        # notification classes
        self.send_customer_notification(customer['email'], f"Order {order_id} is being processed")
        self.send_admin_notification(f"New order processing: {order_id}")

        return True

    def cancel_order(self, order_id):
        logger.info(f"Cancelling order: {order_id}")
        
        order = self.get_order(order_id)
        customer = self.get_customer(order)

        for item in order['items']:    
            product = self.get_product(item)
            self.stock_addition(product, item)

        self.order_cancelled_details(order)

        self.database_operations(order)

        active_orders = [current_order for current_order in active_orders if current_order['id'] != order_id]
        processing_queue = [id for id in processing_queue if id != order_id]

        self.send_customer_notification(customer['email'], f"Order {order_id} has been cancelled")
        self.send_admin_notification(f"Order cancelled: {order_id}")

        return True
    
    def update_order(self, order_id, updation_operation):
        print(f"Updating order: {order_id}")
        
        try:
            if updation_operation:
                order = self.get_order(order_id)
                customer = self.get_customer(order)

                if updation_operation == "Cancel":
                    self.cancel_order(order_id)
                elif updation_operation == "Addition":
                    self.process_order(order_id)
                else:
                    raise ValueError
        except Exception as e:
            logger.info("Problem in updating order!!")



    # class notification
    # def send_customer_notification(self, email, message):
    #     try:
    #         logger.info(f"Sending email to {email}: {message}")
    #     except Exception as e:
    #         logger.info("Failed to send customer notification")
    #         logger.info(e)

    # def send_admin_notification(self, message):
    #     try:
    #         logger.info(f"Admin notification: {message}")
    #     except:
    #         logger.info("Failed to send admin notification")

    # def add_customer(self, customer):
    #     try:
    #         if customer.get('id') or customer.get('email'):
    #             self.customers[customer['id']] = customer
    #     except Exception as e:
    #         logger.info("Failed to add customer")
    #     else:
    #         return True

    # def add_product(self, product):
    #     try:
    #         if product.get('id') or product.get('price', 0) < 0:
    #             self.products[product['id']] = product
    #     except (ValueError, TypeError) as e:
    #         logger.info("Failed to add product")
    #     else:
    #         return True

    # def generate_order_report(self, start_date, end_date):
    #     report = "Order Report\n"
    #     total_orders = 0
    #     total_revenue = 0

    #     for order in self.order_database.values():
    #         if order['created_at'] >= start_date and order['created_at'] <= end_date:
    #             if order['status'] != 'cancelled':
    #                 total_orders += 1
    #                 total_revenue += order['final_amount']
                    
    #                 customer = self.customers.get(order['customer_id'])
    #                 if customer:
    #                     report += f"\nOrder ID: {order['id']}"
    #                     report += f"\nCustomer: {customer['name']}"
    #                     report += f"\nAmount: ${order['final_amount']}"
    #                     report += f"\nStatus: {order['status']}"
    #                     report += f"\n-------------------"

    #     report += f"\n\nTotal Orders: {total_orders}"
    #     report += f"\nTotal Revenue: ${total_revenue}"
    #     return report

def main():
    processor = OrderProcessor()

    processor.add_customer({
        'id': 'CUST1',
        'name': 'John Doe',
        'email': 'john@example.com',
        'address': '123 Main St',
        'phone': '555-0123',
        'membership_level': 'gold',
        'order_history': []
    })

    processor.add_product({
        'id': 'PROD1',
        'name': 'Widget',
        'price': 99.99,
        'description': 'A fantastic widget',
        'category': 'gadgets',
        'stock': 100,
        'is_active': True
    })

    order_id = 'ORD123'
    result = processor.process_order(order_id)
    print(f"Order processing {'succeeded' if result else 'failed'}")

if __name__ == "__main__":
    main()