from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


# Асинхронный движок для бд
async_engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
# Синхронный движок для бд
sync_engine = create_engine(settings.SYNC_DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
sync_session_factory = sessionmaker(sync_engine, expire_on_commit=False, class_=Session)
