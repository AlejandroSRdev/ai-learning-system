import asyncio
import logging
import socket

import asyncpg
from src.config import settings

logger = logging.getLogger(__name__)


async def init_pool() -> asyncpg.Pool:
    try:
        return await asyncpg.create_pool(settings.database_url, ssl="require")
    except (socket.gaierror, OSError) as e:
        msg = "Database connection failed: hostname could not be resolved. Check DATABASE_URL host. Possible IPv6 / DNS mismatch."
        logger.error(msg)
        raise RuntimeError(msg) from e
    except asyncpg.InvalidPasswordError as e:
        msg = "Database connection failed: authentication error. Check DATABASE_URL credentials."
        logger.error(msg)
        raise RuntimeError(msg) from e
    except asyncio.TimeoutError as e:
        msg = "Database connection failed: network timeout. Check connectivity and firewall rules."
        logger.error(msg)
        raise RuntimeError(msg) from e
    except Exception as e:
        msg = f"Database connection failed: unexpected error — {type(e).__name__}: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e


async def close_pool(pool: asyncpg.Pool) -> None:
    await pool.close()