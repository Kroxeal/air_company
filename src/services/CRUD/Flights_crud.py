from datetime import datetime

from src.db.models import Flight, PatchFlight, FlightAll, FlightModel, SearchFlight
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_flight_raw(flight: Flight):
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
        $8
    )
    '''
    values = (
        flight.flight_number,
        flight.departure_datetime,
        flight.arrival_datetime,
        flight.departure_airport,
        flight.arrival_airport,
        int(flight.available_seats),
        float(flight.ticket_price),
        flight.aircraft
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
    ticket_price = COALESCE($7, ticket_price),
    aircraft_id = COALESCE($8, aircraft_id)
    WHERE
    flight_number = $9   
    '''
    values = (
        flight.flight_number,
        flight.departure_datetime,
        flight.arrival_datetime,
        flight.departure_airport,
        flight.arrival_airport,
        flight.available_seats,
        flight.ticket_price,
        flight.aircraft,
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


@db_connection
async def get_all_flight_raw():
    query = '''
    SELECT 
        flights.id,
        flights.flight_number,
        flights.departure_datetime,
        flights.departure_airport,
        flights.arrival_datetime,
        flights.arrival_airport,
        flights.available_seats - COALESCE(seats.count, 0) as available_seats,
        flights.ticket_price,
        aircrafts.name || ' ' || aircrafts.model as aircraft
    FROM Flights
    INNER JOIN Aircrafts ON flights.aircraft_id = aircrafts.id
    LEFT JOIN (
        SELECT flight_id, count(*) as count
        FROM tickets
        GROUP BY flight_id
    ) as seats ON flights.id = seats.flight_id
    '''
    results = await database.fetchall(query)
    flight_lst = []

    for result in results:

        flight_dict = {
            'id': result['id'],
            'flight_number': result['flight_number'],
            'departure_datetime': result['departure_datetime'],
            'departure_airport': result['departure_airport'],
            'arrival_datetime': result['arrival_datetime'],
            'arrival_airport': result['arrival_airport'],
            'available_seats': result['available_seats'],
            'ticket_price': result['ticket_price'],
            'aircraft': result['aircraft'],
        }

        flight_lst.append(FlightAll(**flight_dict))
    print(flight_lst)
    return flight_lst


@db_connection
async def get_flight_by_id(id: str):
    query = '''
    SELECT 
        flights.id,
        flights.flight_number,
        flights.departure_datetime,
        flights.departure_airport,
        flights.arrival_datetime,
        flights.arrival_airport,
        flights.available_seats - COALESCE(seats.count, 0) as available_seats,
        flights.ticket_price,
        aircrafts.name || ' ' || aircrafts.model as aircraft
    FROM Flights
    INNER JOIN Aircrafts ON flights.aircraft_id = aircrafts.id
    LEFT JOIN (
        SELECT flight_id, count(*) as count
        FROM tickets
        GROUP BY flight_id
    ) as seats ON flights.id = seats.flight_id
    WHERE flights.id = $1;
    '''
    values = (
        id,
    )
    result = await database.fetchrow(query, *values)
    return FlightAll(**result) if result else None


@db_connection
async def get_all_flight_form():
    query = '''
    SELECT 
        flights.id,
        flights.departure_airport,
        flights.arrival_airport,
        flights.departure_datetime,
        flights.arrival_datetime
    FROM flights        
    '''
    results = await database.fetchall(query)
    flight_lst = []
    for result in results:
        flight_dict = {
            'id': result['id'],
            'departure_airport': result['departure_airport'],
            'departure_datetime': result['departure_datetime'],
            'arrival_datetime': result['arrival_datetime'],
            'arrival_airport': result['arrival_airport'],
        }
        flight_lst.append(FlightModel(**flight_dict))
    return flight_lst


@db_connection
async def select_price(flight_id: str):

    query = '''
    SELECT ticket_price FROM flights
    WHERE id = $1
    '''
    values = (
        flight_id,
    )
    result = await database.fetchrow(query, *values)
    print(result)
    return result


@db_connection
async def search_flight_raw(flight: SearchFlight):
    query = '''
    SELECT 
        flights.id,
        flights.flight_number,
        flights.departure_datetime,
        flights.departure_airport,
        flights.arrival_datetime,
        flights.arrival_airport,
        flights.available_seats - COALESCE(seats.count, 0) as available_seats,
        flights.ticket_price,
        aircrafts.name || ' ' || aircrafts.model as aircraft 
    FROM flights
    INNER JOIN Aircrafts ON flights.aircraft_id = aircrafts.id
    LEFT JOIN (
        SELECT flight_id, count(*) as count
        FROM tickets
        GROUP BY flight_id
    ) as seats ON flights.id = seats.flight_id
    WHERE 
        departure_airport = COALESCE($1, departure_airport) AND
        arrival_airport = COALESCE($2, arrival_airport) AND
        arrival_datetime = COALESCE($3, arrival_datetime) AND
        departure_datetime >= COALESCE($4, departure_datetime)
    '''
    values = (
        flight.departure_airport,
        flight.arrival_airport,
        flight.arrival_datetime,
        flight.departure_datetime,
    )
    results = await database.fetchall(query, *values)
    flight_lst = []

    for result in results:
        flight_dict = {
            'id': result['id'],
            'flight_number': result['flight_number'],
            'departure_datetime': result['departure_datetime'],
            'departure_airport': result['departure_airport'],
            'arrival_datetime': result['arrival_datetime'],
            'arrival_airport': result['arrival_airport'],
            'available_seats': result['available_seats'],
            'ticket_price': result['ticket_price'],
            'aircraft': result['aircraft'],
        }

        flight_lst.append(FlightAll(**flight_dict))
    print(flight_lst)
    return flight_lst

