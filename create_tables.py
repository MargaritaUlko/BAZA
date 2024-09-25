from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.models.models import user, role  # Убедитесь, что модели импортированы

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async def create_tables():
    async with engine.begin() as conn:
        # Создайте все таблицы
        await conn.run_sync(user.metadata.create_all)

import asyncio
asyncio.run(create_tables())
