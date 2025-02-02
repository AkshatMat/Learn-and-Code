from dataclasses import dataclass
from abc import ABC, abstractmethod
import sqlite3
import csv
from io import StringIO

@dataclass
class Customer:
    customer_id: int
    company_name: str
    contact_name: str
    country: str

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

class ICustomerSearch(ABC):
    @abstractmethod
    def search(self, search_term):
        pass

class CustomerSearchByCountry(ICustomerSearch):
    def __init__(self, db_connection):
        self.db = db_connection

    def search(self, country):
        with self.db as cursor:
            cursor.execute("""
                SELECT customer_id, company_name, contact_name, country 
                FROM customers 
                WHERE country LIKE ? 
                ORDER BY customer_id ASC
            """, (f'%{country}%',))
            
            return [Customer(*row) for row in cursor.fetchall()]

class CustomerSearchByCompany(ICustomerSearch):
    def __init__(self, db_connection):
        self.db = db_connection

    def search(self, company):
        with self.db as cursor:
            cursor.execute("""
                SELECT customer_id, company_name, contact_name, country 
                FROM customers 
                WHERE company_name LIKE ? 
                ORDER BY customer_id ASC
            """, (f'%{company}%',))
            
            return [Customer(*row) for row in cursor.fetchall()]

class CustomerSearchByContact(ICustomerSearch):
    def __init__(self, db_connection):
        self.db = db_connection

    def search(self, contact):
        with self.db as cursor:
            cursor.execute("""
                SELECT customer_id, company_name, contact_name, country 
                FROM customers 
                WHERE contact_name LIKE ? 
                ORDER BY customer_id ASC
            """, (f'%{contact}%',))
            
            return [Customer(*row) for row in cursor.fetchall()]

class CustomerDataExporter:
    @staticmethod
    def export_to_csv(customers):
        output = StringIO()
        writer = csv.writer(output)
        
        for customer in customers:
            writer.writerow([
                customer.customer_id,
                customer.company_name,
                customer.contact_name,
                customer.country
            ])
            
        return output.getvalue()

class CustomerSearchFacade:
    def __init__(self, db_path):
        self.db_connection = DatabaseConnection(db_path)
        self.country_search = CustomerSearchByCountry(self.db_connection)
        self.company_search = CustomerSearchByCompany(self.db_connection)
        self.contact_search = CustomerSearchByContact(self.db_connection)
        self.exporter = CustomerDataExporter()
    
    def search_by_country(self, country):
        return self.country_search.search(country)
    
    def search_by_company(self, company):
        return self.company_search.search(company)
    
    def search_by_contact(self, contact):
        return self.contact_search.search(contact)
    
    def export_to_csv(self, customers) :
        return self.exporter.export_to_csv(customers)

if __name__ == "__main__":
    search_facade = CustomerSearchFacade("customers.db")
    
    customers = search_facade.search_by_country("USA")
    
    csv_data = search_facade.export_to_csv(customers)