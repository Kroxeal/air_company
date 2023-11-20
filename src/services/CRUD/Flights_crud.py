from datetime import datetime

from src.db.models import Flight, PatchFlight
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_flight_raw(model: str, flight: Flight):
    query = '''
    INSERT INTO
    flights (
        flight_number,
        departure_datetime,
        arrival_datetime,
        departure_airport,
        arrival_airport,
        available_seats,
        ticket_price,
        aircraft_id
    )
    VALUES(
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        (SELECT id FROM aircrafts WHERE model = $8)
    )
    '''
    values = (
        flight.flight_number,
        flight.departure_datetime,
        flight.arrival_datetime,
        flight.departure_airport,
        flight.arrival_airport,
        flight.available_seats,
        flight.ticket_price,
        model,
    )
    await database.execute(query, *values)
    return flight


@db_connection
async def get_flight_raw(flight_number: str):
    query = '''
    SELECT * FROM flights
    WHERE flight_number = $1
    '''
    values = (
        flight_number,
    )

    result = await database.fetchrow(query, *values)
    return Flight(**result)


@db_connection
async def update_flight_partially_raw(flight_number: str, flight: PatchFlight):
    query = '''
    UPDATE flights
    SET
    flight_number = COALESCE($1, flight_number),
    departure_datetime = COALESCE($2, departure_datetime),
    arrival_datetime = COALESCE($3, arrival_datetime),
    departure_airport = COALESCE($4, departure_airport),
    arrival_airport = COALESCE($5, arrival_airport),
    available_seats = COALESCE($6, available_seats),
    ticket_price = COALESCE($7, ticket_price)
    WHERE
    flight_number = $8   
    '''
    values = (
        flight.flight_number,
        flight.departure_datetime,
        flight.arrival_datetime,
        flight.departure_airport,
        flight.arrival_airport,
        flight.available_seats,
        flight.ticket_price,
        flight_number,
    )

    await database.execute(query, *values)
    return flight


@db_connection
async def delete_flight_raw(flight_number: str):
    query = '''
    DELETE FROM flights
    WHERE
    flight_number = $1
    '''
    values = (
        flight_number,
    )

    await database.execute(query, *values)
    return f'Flight {flight_number} deleted'



