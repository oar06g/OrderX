from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from src.settings import DB_URL

class AsyncDatabase:
    _engine = None
    _session_factory = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_async_engine(
                DB_URL,
                echo=True,
                pool_pre_ping=True,
                pool_recycle=280,
            )
        return cls._engine
    
    @classmethod
    def get_session_factory(cls):
        if cls._session_factory is None:
            engine = cls.get_engine()
            cls._session_factory = sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )
        return cls._session_factory
    
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncDatabase.get_session_factory()
    async with async_session() as session:
        yield session