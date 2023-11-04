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
    query_params = [username]

    if user.name is not None:
        query_params.append(user.name)
        name_update = "name = $2"
    else:
        name_update = ""

    if user.surname is not None:
        query_params.append(user.surname)
        surname_update = "surname = $3"
    else:
        surname_update = ""

    if user.email is not None:
        query_params.append(user.email)
        email_update = "email = $%d" % (len(query_params))
    else:
        email_update = ""

    if user.phone_number is not None:
        query_params.append(user.phone_number)
        phone_number_update = "phone_number = $%d" % (len(query_params))
    else:
        phone_number_update = ""

    update_query = f"""
    UPDATE users
    SET {', '.join(filter(None, [
        name_update,
        surname_update,
        email_update,
        phone_number_update
    ]))}
    WHERE username = $1
    """
    print(update_query)
    print(*query_params)

    result = await database.execute(update_query, *query_params)
    print(result)
    updated_user = await database.fetchrow(
        "SELECT * FROM users WHERE username = $1",
        username
    )

    return User(**updated_user)



