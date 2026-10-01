from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    stocks = relationship("Stock", back_populates="warehouse")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    price = Column(Float)

    stocks = relationship("Stock", back_populates="product")

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)

    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    warehouse = relationship("Warehouse", back_populates="stocks")
    product = relationship("Product", back_populates="stocks") 
