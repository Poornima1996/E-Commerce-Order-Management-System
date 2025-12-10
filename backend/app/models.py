"""
Database models for the e-commerce application
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_description = Column(Text)
    
    # Relationship to order mappings
    order_mappings = relationship("OrderProductMap", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}')>"


class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_description = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    
    # Relationship to order mappings
    order_mappings = relationship("OrderProductMap", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, description='{self.order_description}')>"


class OrderProductMap(Base):
    """Order-Product mapping model"""
    __tablename__ = "order_product_map"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    order = relationship("Order", back_populates="order_mappings")
    product = relationship("Product", back_populates="order_mappings")

    def __repr__(self):
        return f"<OrderProductMap(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"

