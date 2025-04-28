class ReportGeneration:
    def __init__(self,start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def generate_order_report(self, start_date, end_date):
        report = "Order Report\n"
        total_orders = 0
        total_revenue = 0

        for order in self.order_database.values():
            if order['created_at'] >= self.start_date and order['created_at'] <= self.end_date:
                if order['status'] != 'cancelled':
                    total_orders += 1
                    total_revenue += order['final_amount']
                    
                    customer = self.customers.get(order['customer_id'])
                    if customer:
                        report += f"\nOrder ID: {order['id']}"
                        report += f"\nCustomer: {customer['name']}"
                        report += f"\nAmount: ${order['final_amount']}"
                        report += f"\nStatus: {order['status']}"
                        report += f"\n-------------------"

        report += f"\n\nTotal Orders: {total_orders}"
        report += f"\nTotal Revenue: ${total_revenue}"
        return report