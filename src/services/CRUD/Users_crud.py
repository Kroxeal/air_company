from fastapi import HTTPException

from src.db.models import User, UserResponse, BaseUser, UserPatch, UserID
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


@db_connection
async def get_user_with_id(username: str):
    query = 'SELECT * FROM users WHERE username = $1'
    result = await database.fetchrow(query, username)
    if result:
        user = UserID(**result)
        return user
    else:
        raise HTTPException(status_code=400, detail="There's no such a user")


@db_connection
async def update_user(username: str, user: BaseUser):
    query = '''
    UPDATE users
    SET name = $1, surname = $2, phone_number = $3, email = $4
    WHERE username = $5
    '''
    values = (
        user.name,
        user.surname,
        user.phone_number,
        user.email,
        username
    )

    await database.execute(query, *values)
    return user


@db_connection
async def update_user_partially(username: str, user: UserPatch):
    query = '''
    UPDATE users
    SET
    name = COALESCE($1, name),
    surname = COALESCE($2, surname),
    phone_number = COALESCE($3, phone_number),
    email = COALESCE($4, email)
    WHERE
    username = $5
    '''
    values = (
        user.name,
        user.surname,
        user.phone_number,
        user.email,
        username,
    )
    await database.execute(query, *values)
    return user


@db_connection
async def delete_user_f(username: str):
    query = '''
    DELETE FROM users
    WHERE username = $1
    '''
    values = (
        username,
    )
    await database.execute(query, *values)
    return f'User {username} deleted'
