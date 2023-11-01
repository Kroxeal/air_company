from functools import wraps

from src.db.settings import database


def db_connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await database.connect()
            return await func(*args, **kwargs)
        finally:
            await database.disconnect()
    return wrapper
