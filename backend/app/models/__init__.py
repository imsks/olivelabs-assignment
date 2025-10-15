from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    segment = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    """Product model"""
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_line = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="product")

class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    region = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    
    @property
    def revenue(self) -> float:
        """Calculate revenue for this order"""
        return self.quantity * self.unit_price
