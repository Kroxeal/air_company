from fastapi import HTTPException

from src.db.models import User
from src.db.settings import database
from src.services.password_hash import HashingPassword
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_user(user: User):
    hashed_password = HashingPassword.password_to_hash(user.password)
    query = """
    INSERT INTO Users (
        username,
        name,
        surname,
        phone_number,
        email,
        password
        )
    VALUES ($1, $2, $3, $4, $5, $6)
    """
    values = (
        user.username,
        user.name,
        user.surname,
        user.phone_number,
        user.email,
        hashed_password,
    )

    await database.execute(query, *values)

    return user


@db_connection
async def get_user(username: str):
    query = 'SELECT * FROM users WHERE username = $1'
    result = await database.fetchrow(query, username)
    if result:
        user = User(**result)
        return user
    else:
        raise HTTPException(status_code=400, detail="There's no such a user")
