"""
Seed data script for NLQ application
Generates sample business data for orders, customers, and products
"""

import random
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Customer, Product, Order

def generate_sample_data():
    """Generate sample data for the database"""
    
    # Sample data
    customers_data = [
        {"name": "Acme Corp", "segment": "Enterprise", "country": "USA"},
        {"name": "TechStart Inc", "segment": "SMB", "country": "Canada"},
        {"name": "Global Solutions", "segment": "Enterprise", "country": "UK"},
        {"name": "Innovation Labs", "segment": "SMB", "country": "Germany"},
        {"name": "Data Dynamics", "segment": "Enterprise", "country": "USA"},
        {"name": "CloudFirst", "segment": "SMB", "country": "Australia"},
        {"name": "NextGen Systems", "segment": "Enterprise", "country": "Japan"},
        {"name": "Agile Works", "segment": "SMB", "country": "India"},
    ]
    
    products_data = [
        {"product_line": "Software", "category": "Enterprise Software"},
        {"product_line": "Hardware", "category": "Servers"},
        {"product_line": "Software", "category": "Cloud Services"},
        {"product_line": "Hardware", "category": "Storage"},
        {"product_line": "Software", "category": "Analytics"},
        {"product_line": "Hardware", "category": "Networking"},
        {"product_line": "Software", "category": "Security"},
        {"product_line": "Hardware", "category": "Workstations"},
    ]
    
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
    
    db = SessionLocal()
    
    try:
        # Create customers
        customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        
        # Create products
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        
        db.commit()
        
        # Create orders
        start_date = date(2023, 1, 1)
        end_date = date(2024, 12, 31)
        
        for _ in range(1000):  # Generate 1000 orders
            order_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            
            order = Order(
                customer_id=random.choice(customers).customer_id,
                product_id=random.choice(products).product_id,
                order_date=order_date,
                quantity=random.randint(1, 100),
                unit_price=round(random.uniform(10.0, 1000.0), 2),
                region=random.choice(regions)
            )
            db.add(order)
        
        db.commit()
        print("Sample data generated successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error generating sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_sample_data()
