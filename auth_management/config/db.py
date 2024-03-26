import os

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# if os.getenv("ENVIRONMENT") == "docker":
#     DATABASE_URL = os.environ.get("DATABASE_URL")
# else:
#     DATABASE_URL = os.environ.get("DEVELOPMENT_DATABASE_URL")

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))


async def initialize_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
