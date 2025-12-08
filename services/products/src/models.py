from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(250), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    sku = Column(String(100), unique=True, nullable=True)