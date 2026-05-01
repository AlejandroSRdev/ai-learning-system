import asyncpg
from src.config import settings


async def init_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(settings.database_url, ssl="require")


async def close_pool(pool: asyncpg.Pool) -> None:
    await pool.close()
