from src.db.models import Aircraft, PatchAircraft
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_aircraft_raw(aircraft: Aircraft):
    query = '''
    INSERT INTO aircrafts(
    name,
    model,
    year_manufacture,
    seating_capacity,
    max_range,
    engine_type,
    status,
    last_service,
    manufacture
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    '''
    values = (
        aircraft.name,
        aircraft.model,
        aircraft.year_manufacture,
        aircraft.seating_capacity,
        aircraft.max_range,
        aircraft.engine_type,
        aircraft.status,
        aircraft.last_service,
        aircraft.manufacture,
    )
    await database.execute(query, *values)
    return aircraft


@db_connection
async def get_aircraft_raw(model: str):
    query = '''
    SELECT * FROM aircrafts
    WHERE model = $1
    '''
    values = (
        model,
    )

    result = await database.fetchrow(query, *values)
    return Aircraft(**result)


@db_connection
async def update_aircraft_partially_raw(model: str, aircraft: PatchAircraft):
    query = '''
    UPDATE aircrafts
    SET
    name = COALESCE($1, name),
    model = COALESCE($2, model),
    year_manufacture = COALESCE($3, year_manufacture),
    seating_capacity = COALESCE($4, seating_capacity),
    max_range = COALESCE($5, max_range),
    engine_type = COALESCE($6, engine_type),
    status = COALESCE($7, status),
    last_service = COALESCE($8, last_service)
    WHERE model = $9
    '''
    values = (
        aircraft.name,
        aircraft.model,
        aircraft.year_manufacture,
        aircraft.seating_capacity,
        aircraft.max_range,
        aircraft.engine_type,
        aircraft.status,
        aircraft.last_service,
        model,
    )
    await database.execute(query, *values)
    return aircraft


@db_connection
async def delete_aircraft_raw(model: str):
    query = '''
    DELETE FROM
    aircrafts
    WHERE model = $1
    '''
    values = (
        model,
    )
    await database.execute(query, *values)
    return f'Aircraft {model} deleted'


@db_connection
async def get_all_aircrafts_f():
    query = '''
    SELECT * FROM aircrafts;
    '''
    results = await database.fetchall(query)
    aircrafts_lst = []
    for result in results:
        aircrafts_dict = {
            'name': result['name'],
            'model': result['model'],
            'year_manufacture': result['year_manufacture'],
            'seating_capacity': result['seating_capacity'],
            'max_range': result['max_range'],
            'engine_type': result['engine_type'],
            'status': result['status'],
            'last_service': result['last_service'],
            'manufacture': result['manufacture'],
            'registration_number': result['registration_number'],
        }
        aircrafts_lst.append(Aircraft(**aircrafts_dict))
    print({'aircrafts': aircrafts_lst})
    return aircrafts_lst
