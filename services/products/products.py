from fastapi import FastAPI, HTTPException, Depends, Query, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from typing import List, Optional

from src.database import get_db, AsyncDatabase
from src.models import Base, Product
from src.settings import DB_URL
from src.schemas import *
from src.auth import decode_jwt_token

app = FastAPI(title="Product Service")
bearer_scheme = HTTPBearer()


# ------------------------
#  INIT DATABASE
# ------------------------
async def init_db():
    engine = create_async_engine(DB_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    engine = AsyncDatabase.get_engine()
    await engine.dispose()


# ------------------------
#  AUTH MIDDLEWARE
# ------------------------
def require_auth(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    print(token)
    payload = decode_jwt_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# ------------------------
#  ENDPOINTS
# ------------------------

@app.get("/products", response_model=List[ProductOut])
async def list_products(
    q: Optional[str] = Query(None),
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * limit
    stmt = select(Product)

    if q:
        stmt = stmt.where(Product.title.ilike(f"%{q}%"))

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return items


@app.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=ProductOut)
async def create_product(
    payload: ProductCreate,
    user=Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    product = Product(**payload.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@app.put("/products/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    user=Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


@app.patch("/products/{product_id}/stock", response_model=ProductOut)
async def change_stock(
    product_id: int,
    stock: int,
    user=Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock = stock
    await db.commit()
    await db.refresh(product)
    return product


@app.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    user=Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"ok": True}
