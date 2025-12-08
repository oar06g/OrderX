from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    sku: Optional[str] = None

class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    sku: Optional[str]

class ProductOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    stock: int
    sku: Optional[str]

    class Config:
        from_attributes = True
