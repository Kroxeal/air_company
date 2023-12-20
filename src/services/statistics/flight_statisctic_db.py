from datetime import datetime

from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def get_all_flight_statistics():
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
        aircrafts.name || ' ' || aircrafts.model as aircraft,
        aircrafts.registration_number
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
            'registration_number': result['registration_number'],

        }
        flight_lst.append(flight_dict)
    print(flight_lst)
    return flight_lst


@db_connection
async def import_json_flight(data):
    for record in data:
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
                (select aircrafts.id from aircrafts
                 where registration_number = $8)
            )
            '''
        values = (
            record['flight_number'],
            datetime.fromisoformat(record['departure_datetime']),
            datetime.fromisoformat(record['arrival_datetime']),
            record['departure_airport'],
            record['arrival_airport'],
            record['available_seats'],
            record['ticket_price'],
            record['aircraft_number']
        )

        await database.execute(query, *values)


@db_connection
async def export_json_flights():
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
        aircrafts.name || ' ' || aircrafts.model as aircraft,
        aircrafts.registration_number
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
            'registration_number': result['registration_number'],
        }

        flight_lst.append(flight_dict)
    print(flight_lst)
    return flight_lst
