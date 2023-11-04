from fastapi import HTTPException
from pydantic import UUID4

from src.db.models import BasePassport, CreatePassport
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_passport(user_id, passport: BasePassport):
    insert_query = """
    INSERT INTO Passports (
    passport_number,
    nationality,
    sex,
    address,
    date_of_birth,
    date_of_issue,
    date_of_expire,
    user_id
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """
    values = (
        passport.passport_number,
        passport.nationality,
        passport.sex,
        passport.address,
        passport.date_of_birth,
        passport.date_of_issue,
        passport.date_of_expire,
        user_id
    )

    await database.execute(insert_query, *values)

    return passport


@db_connection
async def get_passport(passport_number: str):
    query = 'SELECT * FROM passports WHERE passport_number = $1'
    result = await database.fetchrow(query, passport_number)
    if result:
        passport = BasePassport(**result)
        return passport
    else:
        raise HTTPException(status_code=400, detail="There's no such a user")


@db_connection
async def get_passport_by_id(user_id: str):
    query = 'SELECT * FROM passports WHERE user_id = $1'
    result = await database.fetchrow(query, user_id)
    if result:
        passport = BasePassport(**result)
        return passport
    else:
        raise HTTPException(status_code=400, detail="There's no such a user")


# this part is not work now!!
@db_connection
async def update_passport(user_id: str, passport: CreatePassport):
    query = '''
    UPDATE passports
    SET 
    nationality = $1,
    sex = $2,
    address = $3,
    date_of_birth = $4,
    date_of_issue = $5,
    date_of_expire = $6
    WHERE user_id = $7
    '''
    values = (
        passport.nationality,
        passport.sex,
        passport.address,
        passport.date_of_birth,
        passport.date_of_issue,
        passport.date_of_expire,
        user_id
    )

    await database.execute(query, *values)
    return passport


@db_connection
async def update_current_passport_partially(user_id: str, passport: CreatePassport):
    query_params = [user_id]

    if passport.passport_number is not None:
        query_params.append(passport.passport_number)
        passport_number_update = "passport_number = $2"
    else:
        passport_number_update = ""

    if passport.nationality is not None:
        query_params.append(passport.nationality)
        nationality_update = "nationality = $3"
    else:
        nationality_update = ""

    if passport.sex is not None:
        query_params.append(passport.sex)
        sex_update = "sex = $4"
    else:
        sex_update = ""

    if passport.address is not None:
        query_params.append(passport.address)
        address_update = "address = $5"
    else:
        address_update = ""

    if passport.date_of_birth is not None:
        query_params.append(passport.date_of_birth)
        date_of_birth_update = "date_of_birth = $6"
    else:
        date_of_birth_update = ""

    if passport.date_of_issue is not None:
        query_params.append(passport.date_of_issue)
        date_of_issue_update = "date_of_issue = $7"
    else:
        date_of_issue_update = ""

    if passport.date_of_expire is not None:
        query_params.append(passport.date_of_expire)
        date_of_expire_update = "date_of_expire = $8"
    else:
        date_of_expire_update = ""

    if passport.photo is not None:
        query_params.append(passport.photo)
        photo_update = "photo = $9"
    else:
        photo_update = ""

    update_query = f"""
    UPDATE passports
    SET {', '.join(filter(None, [
        passport_number_update,
        nationality_update,
        sex_update,
        address_update,
        date_of_birth_update,
        date_of_issue_update,
        date_of_expire_update,
        photo_update
    ]))}
    WHERE user_id = $1
    """

    print(update_query)
    print(*query_params)

    result = await database.execute(update_query, *query_params)
    print(result)
    updated_user = await database.fetchrow(
        "SELECT * FROM passports WHERE user_id = $1",
        user_id
    )

    return CreatePassport(**updated_user)
