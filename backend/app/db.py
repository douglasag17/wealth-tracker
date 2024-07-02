from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///database.db"
async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    max_overflow=-1,
    connect_args={"timeout": 120},
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
