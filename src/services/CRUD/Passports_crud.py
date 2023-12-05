from fastapi import HTTPException

from src.db.models import BasePassport, CreatePassport, PassportUsername
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_passport(passport: PassportUsername, filename):
    print("crud")
    insert_query = """
    INSERT INTO Passports (
    passport_number,
    nationality,
    sex,
    address,
    date_of_birth,
    date_of_issue,
    date_of_expire,
    user_id,
    photo
    )
    VALUES (
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        (SELECT id FROM users WHERE username = $8),
        $9
    )
    """
    values = (
        passport.passport_number,
        passport.nationality,
        passport.sex,
        passport.address,
        passport.date_of_birth,
        passport.date_of_issue,
        passport.date_of_expire,
        passport.username,
        filename
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


@db_connection
async def update_passport(username: str, passport: CreatePassport):
    query = '''
    UPDATE passports
    SET 
    nationality = $1,
    sex = $2,
    address = $3,
    date_of_birth = $4,
    date_of_issue = $5,
    date_of_expire = $6
    WHERE user_id = (
    SELECT id FROM users WHERE username = $7
    )
    '''
    values = (
        passport.nationality,
        passport.sex,
        passport.address,
        passport.date_of_birth,
        passport.date_of_issue,
        passport.date_of_expire,
        username
    )

    await database.execute(query, *values)
    return passport


@db_connection
async def update_current_passport_partially(passport_number: str, passport: CreatePassport, uploaded_file: str):
    query = '''
        UPDATE passports
        SET 
        passport_number = COALESCE($1, passport_number),
        nationality = COALESCE($2, nationality),
        sex = COALESCE($3, sex),
        address = COALESCE($4, address),
        date_of_birth = COALESCE($5, date_of_birth),
        date_of_issue = COALESCE($6, date_of_issue),
        date_of_expire = COALESCE($7, date_of_expire),
        photo = COALESCE($8, photo)
        WHERE
        passport_number = $9
    '''
    values = (
        passport.passport_number,
        passport.nationality,
        passport.sex,
        passport.address,
        passport.date_of_birth,
        passport.date_of_issue,
        passport.date_of_expire,
        uploaded_file,
        passport_number,
    )
    await database.execute(query, *values)
    return passport


@db_connection
async def delete_passport_f(passport_number: str):
    query = '''
    DELETE FROM passports
    WHERE
    passport_number = $1
    '''
    values = (
        passport_number,
    )
    await database.execute(query, *values)
    return f"{passport_number}'s passport deleted"


@db_connection
async def get_all_passports_f():
    query = '''
    SELECT * FROM passports
    '''
    results = await database.fetchall(query)
    print({'result': results})
    passports_data_list = []

    for result in results:
        photo_filename = result['photo']
        photo_route = f"/static/images/{photo_filename}"
        passport_data = {

            'passport_number': result['passport_number'],
            'nationality': result['nationality'],
            'sex': result['sex'],
            'address': result['address'],
            'date_of_birth': result['date_of_birth'],
            'date_of_issue': result['date_of_issue'],
            'date_of_expire': result['date_of_expire'],
            'photo': photo_route,
        }
        passports_data_list.append(CreatePassport(**passport_data))
    print({'passport': passports_data_list})
    return passports_data_list
