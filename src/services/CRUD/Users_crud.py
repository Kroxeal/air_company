from fastapi import HTTPException

from src.db.models import User, UserResponse, BaseUser, UserPatch, UserID, PostUser
from src.db.settings import database
from src.services.password_hash import HashingPassword
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_user(user: PostUser):
    hashed_password = HashingPassword.password_to_hash(user.password)
    query = """
    INSERT INTO Users (
        username,
        name,
        surname,
        phone_number,
        email,
        password,
        role
        )
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    values = (
        user.username,
        user.name,
        user.surname,
        user.phone_number,
        user.email,
        hashed_password,
        user.role
    )

    await database.execute(query, *values)

    return user


@db_connection
async def get_user(username: str):
    print('hi 404')
    query = 'SELECT * FROM users WHERE username = $1'
    result = await database.fetchrow(query, username)
    if result:
        user = User(**result)
        print(user)
        return user #huynya
    else:
        raise HTTPException(status_code=404, detail="There's no such a user")


@db_connection
async def get_user_with_id(username: str):
    query = 'SELECT * FROM users WHERE username = $1'
    result = await database.fetchrow(query, username)
    if result:
        user = UserID(**result)
        return user
    else:
        raise HTTPException(status_code=405, detail="There's no such a user")


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
    email = COALESCE($4, email),
    role = COALESCE($5, role)
    WHERE
    username = $6
    '''
    values = (
        user.name,
        user.surname,
        user.phone_number,
        user.email,
        user.role,
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


@db_connection
async def get_all_users():
    print('hello')
    query = '''
    SELECT * FROM
    users
    '''
    try:
        result = await database.fetchall(query)
        print(result)
        return result
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return []
