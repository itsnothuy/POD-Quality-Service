from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Delivery
from ..core.config import get_settings
from typing import AsyncGenerator


# Load settings for Postgres connection
s = get_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{s.postgres_user}:{s.postgres_password}@"
    f"{s.postgres_host}:{s.postgres_port}/"
    f"{s.postgres_db}"
)

# Create SQLAlchemy Async Engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create an async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db() -> None:
    """
    Create tables if they don’t exist. Call this at FastAPI startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an AsyncSession per request.
    Usage in your routes: 
        async def some_endpoint(session: AsyncSession = Depends(get_session))
    """
    async with async_session() as session:
        yield session
