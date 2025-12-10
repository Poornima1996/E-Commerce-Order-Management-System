"""
Database initialization script
Creates tables and seeds initial data
"""
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import Product, Order, OrderProductMap


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


def seed_products(db: Session):
    """Seed initial product data"""
    print("Seeding product data...")
    
    # Check if products already exist
    existing_products = db.query(Product).count()
    if existing_products > 0:
        print(f"Products already exist ({existing_products} products found). Skipping seed.")
        return
    
    # Create initial products as per requirements
    products = [
        Product(id=1, product_name="HP laptop", product_description="This is HP laptop"),
        Product(id=2, product_name="lenovo laptop", product_description="This is lenovo"),
        Product(id=3, product_name="Car", product_description="This is Car"),
        Product(id=4, product_name="Bike", product_description="This is Bike"),
    ]
    
    db.add_all(products)
    db.commit()
    print(f"Successfully seeded {len(products)} products!")


def init_database():
    """Initialize database with tables and seed data"""
    try:
        # Create tables
        create_tables()
        
        # Seed data
        db = SessionLocal()
        try:
            seed_products(db)
        finally:
            db.close()
        
        print("\nDatabase initialization completed successfully!")
        return True
    except Exception as e:
        print(f"\nError initializing database: {str(e)}")
        return False


if __name__ == "__main__":
    init_database()

