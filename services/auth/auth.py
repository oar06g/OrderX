from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from src.database import get_db, AsyncDatabase
from src.models import User, Base
from src.settings import DB_URL
from src.schemas import *
from src.auth import create_jwt_token, hash_password, verify_password

app = FastAPI()

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

@app.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_passw = hash_password(data.password)

    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed_passw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=LoginResponse, status_code=200)
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="This account does not exist"
        )
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            delail="Invalid email or password"
        )
    token = create_jwt_token({"user_id": user.id})

    return LoginResponse(jwt=token)
