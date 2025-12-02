"""
Seed the database with comprehensive test data for orders, inventory, and customers.
Run this script to populate the database with sample data.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.services.order_service.models import Order, OrderItem
from backend.services.inventory_service.models import Inventory
from backend.services.returns_service.models import Return
from datetime import datetime, timedelta

async def seed_database():
    """Populate database with comprehensive sample data"""
    
    # Create synchronous database connection
    DATABASE_URL = "postgresql://user:password@localhost:5432/customer_order_portal"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database with comprehensive test data...")
        print("⚠️  Clearing existing seed data...")
        
        # Clear existing data to avoid conflicts
        db.query(Return).delete()
        db.query(Order).delete()
        db.query(Inventory).delete()
        db.commit()
        print("✓ Cleared existing data")
        
        # 1. Create Inventory Items (22 items across different categories)
        print("Adding inventory items...")
        
        inventory_items = [
            # Laptops
            Inventory(name="Gaming Laptop RTX 4060", sku="GLAP-4060", stock=15, price=1299.99, category="Laptops", reorder_threshold=5),
            Inventory(name="Dell Latitude 15", sku="DELL-LAT15", stock=8, price=899.99, category="Laptops", reorder_threshold=3),
            Inventory(name="Lenovo ThinkPad X1", sku="LNVO-X1", stock=0, price=1499.99, category="Laptops", reorder_threshold=3),
            Inventory(name="HP Pavilion Gaming", sku="HP-PAV-G", stock=12, price=1099.99, category="Laptops", reorder_threshold=5),
            Inventory(name="ASUS ROG Strix", sku="ASUS-ROG", stock=6, price=1899.99, category="Laptops", reorder_threshold=3),
            Inventory(name="MacBook Air M2", sku="MAC-AIR-M2", stock=10, price=1199.99, category="Laptops", reorder_threshold=4),
            
            # Keyboards
            Inventory(name="RGB Mechanical Keyboard", sku="KB-RGB-01", stock=50, price=129.99, category="Keyboards", reorder_threshold=15),
            Inventory(name="Wireless Gaming Keyboard", sku="KB-WL-G", stock=30, price=89.99, category="Keyboards", reorder_threshold=10),
            Inventory(name="Ergonomic Keyboard", sku="KB-ERGO", stock=20, price=79.99, category="Keyboards", reorder_threshold=8),
            Inventory(name="Compact 60% Keyboard", sku="KB-60P", stock=25, price=99.99, category="Keyboards", reorder_threshold=10),
            
            # Mice
            Inventory(name="Wireless Gaming Mouse", sku="MOUSE-WL-G", stock=40, price=69.99, category="Mice", reorder_threshold=12),
            Inventory(name="Ergonomic Vertical Mouse", sku="MOUSE-VERT", stock=18, price=49.99, category="Mice", reorder_threshold=8),
            Inventory(name="RGB Gaming Mouse", sku="MOUSE-RGB", stock=35, price=79.99, category="Mice", reorder_threshold=12),
            
            # Monitors
            Inventory(name="27\" 4K Monitor", sku="MON-27-4K", stock=10, price=399.99, category="Monitors", reorder_threshold=4),
            Inventory(name="34\" Ultrawide Monitor", sku="MON-34-UW", stock=5, price=599.99, category="Monitors", reorder_threshold=3),
            Inventory(name="24\" Gaming Monitor 144Hz", sku="MON-24-144", stock=15, price=299.99, category="Monitors", reorder_threshold=5),
            
            # Accessories
            Inventory(name="USB-C Hub 7-in-1", sku="ACC-HUB-7", stock=45, price=39.99, category="Accessories", reorder_threshold=15),
            Inventory(name="Laptop Stand Aluminum", sku="ACC-STAND", stock=30, price=29.99, category="Accessories", reorder_threshold=10),
            Inventory(name="Wireless Headset", sku="ACC-HS-WL", stock=22, price=89.99, category="Accessories", reorder_threshold=8),
            Inventory(name="Webcam 1080p", sku="ACC-CAM-1080", stock=18, price=59.99, category="Accessories", reorder_threshold=7),
            Inventory(name="External SSD 1TB", sku="ACC-SSD-1TB", stock=25, price=129.99, category="Accessories", reorder_threshold=10),
            Inventory(name="Mechanical Numpad", sku="ACC-NUMPAD", stock=12, price=49.99, category="Accessories", reorder_threshold=5),
        ]
        
        db.add_all(inventory_items)
        db.commit()
        print(f"✓ Added {len(inventory_items)} inventory items")
        
        # 2. Create Sample Orders (15 orders with variety)
        print("Adding sample orders...")
        orders_data = [
            {"id": 1001, "user_id": 1, "status": "DELIVERED", "total_amount": 1429.98, "created_at": datetime.now() - timedelta(days=15)},
            {"id": 1002, "user_id": 2, "status": "PROCESSING", "total_amount": 899.99, "created_at": datetime.now() - timedelta(days=2)},
            {"id": 1003, "user_id": 3, "status": "SHIPPED", "total_amount": 289.97, "created_at": datetime.now() - timedelta(days=5)},
            {"id": 1004, "user_id": 4, "status": "DELIVERED", "total_amount": 599.99, "created_at": datetime.now() - timedelta(days=20)},
            {"id": 1005, "user_id": 5, "status": "PENDING", "total_amount": 399.98, "created_at": datetime.now() - timedelta(hours=6)},
            {"id": 1006, "user_id": 6, "status": "SHIPPED", "total_amount": 498.96, "created_at": datetime.now() - timedelta(days=3)},
            {"id": 1007, "user_id": 7, "status": "DELIVERED", "total_amount": 1899.99, "created_at": datetime.now() - timedelta(days=30)},
            {"id": 1008, "user_id": 8, "status": "PROCESSING", "total_amount": 229.98, "created_at": datetime.now() - timedelta(days=1)},
            {"id": 1009, "user_id": 9, "status": "CANCELLED", "total_amount": 1299.99, "created_at": datetime.now() - timedelta(days=8)},
            {"id": 1010, "user_id": 10, "status": "DELIVERED", "total_amount": 449.97, "created_at": datetime.now() - timedelta(days=12)},
            {"id": 1011, "user_id": 11, "status": "SHIPPED", "total_amount": 1199.99, "created_at": datetime.now() - timedelta(days=4)},
            {"id": 1012, "user_id": 12, "status": "PROCESSING", "total_amount": 169.98, "created_at": datetime.now() - timedelta(hours=12)},
            {"id": 1013, "user_id": 13, "status": "DELIVERED", "total_amount": 689.95, "created_at": datetime.now() - timedelta(days=18)},
            {"id": 1014, "user_id": 14, "status": "PENDING", "total_amount": 299.99, "created_at": datetime.now() - timedelta(hours=2)},
            {"id": 1015, "user_id": 15, "status": "SHIPPED", "total_amount": 959.97, "created_at": datetime.now() - timedelta(days=6)},
        ]
        
        for order_data in orders_data:
            existing = db.query(Order).filter(Order.id == order_data["id"]).first()
            if not existing:
                order = Order(**order_data)
                db.add(order)
        
        db.commit()
        print(f"✓ Added {len(orders_data)} sample orders")
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📊 Sample data summary:")
        print(f"  - Inventory Items: {len(inventory_items)} products across 5 categories")
        print(f"  - Orders: {len(orders_data)} orders with various statuses")
        print("\n🎯 Test scenarios available:")
        print("  - In-stock products: Gaming Laptop, RGB Keyboard, Wireless Mouse, etc.")
        print("  - Out-of-stock: Lenovo ThinkPad X1")
        print("  - Low stock (critical): ASUS ROG Strix (6 units)")
        print("  - Order statuses: DELIVERED, SHIPPED, PROCESSING, PENDING, CANCELLED")
        print("\n💬 Chatbot test queries:")
        print('  - "Do you have gaming laptops in stock?"')
        print('  - "I want to order a keyboard"')
        print('  - "What is the status of order #1003?"')
        print('  - "I need to return order #1001"')
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
