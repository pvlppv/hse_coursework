from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from typing import AsyncGenerator
import models
from settings import get_settings
from base import Base

cfg = get_settings()

engine = create_async_engine(
    cfg.database_url,
    future=True
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(metadata.reflect)  # Reflect tables into metadata


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, models.User)
