# mock/sap_mock.py
import random
import json
from faker import Faker

fake = Faker()

class SAPMockGenerator:
    def __init__(self):
        self.customers = []
        self.products = []
        self.transactions = []
    
    def generate_customer_data(self, count=100):
        """Generate mock customer data that would exist in SAP CRM"""
        for i in range(count):
            customer = {
                "customer_id": f"CUST{10000 + i}",
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.address(),
                "customer_segment": random.choice(["Premium", "Standard", "Budget"]),
                "loyalty_points": random.randint(0, 10000),
                "registration_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
                "last_purchase_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
            }
            self.customers.append(customer)
        return self.customers
    
    def generate_product_data(self, count=50):
        """Generate mock product data that would exist in SAP ERP"""
        categories = ["Electronics", "Clothing", "Home", "Sports", "Books", "Food"]
        for i in range(count):
            category = random.choice(categories)
            product = {
                "product_id": f"PROD{1000 + i}",
                "name": f"{fake.word().capitalize()} {category[:-1] if category.endswith('s') else category}",
                "category": category,
                "base_price": round(random.uniform(10.0, 1000.0), 2),
                "current_stock": random.randint(0, 500),
                "reorder_level": random.randint(10, 50),
                "supplier_id": f"SUPP{100 + random.randint(1, 20)}",
                "description": fake.paragraph(nb_sentences=3)
            }
            self.products.append(product)
        return self.products
    
    def generate_transaction_data(self, count=1000):
        """Generate mock transaction data that would exist in SAP"""
        if not self.customers or not self.products:
            raise Exception("Generate customers and products first")
            
        for i in range(count):
            customer = random.choice(self.customers)
            # Each transaction can have 1-5 products
            num_products = random.randint(1, 5)
            transaction_products = []
            
            for _ in range(num_products):
                product = random.choice(self.products)
                quantity = random.randint(1, 5)
                
                # Apply random discount
                discount = random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2])
                price = product["base_price"] * (1 - discount)
                
                transaction_products.append({
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": round(price, 2),
                    "line_total": round(price * quantity, 2)
                })
            
            transaction_total = sum(item["line_total"] for item in transaction_products)
            
            transaction = {
                "transaction_id": f"TRX{100000 + i}",
                "customer_id": customer["customer_id"],
                "transaction_date": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
                "total_amount": round(transaction_total, 2),
                "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash"]),
                "store_id": f"STORE{random.randint(1, 20)}",
                "items": transaction_products
            }
            self.transactions.append(transaction)
        return self.transactions
    
    def export_to_json(self, filename_prefix="sap_mock_data"):
        """Export all generated data to JSON files"""
        if self.customers:
            with open(f"{filename_prefix}_customers.json", "w") as f:
                json.dump(self.customers, f, indent=2)
        
        if self.products:
            with open(f"{filename_prefix}_products.json", "w") as f:
                json.dump(self.products, f, indent=2)
        
        if self.transactions:
            with open(f"{filename_prefix}_transactions.json", "w") as f:
                json.dump(self.transactions, f, indent=2)
