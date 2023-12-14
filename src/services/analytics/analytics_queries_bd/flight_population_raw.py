from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def population_of_flights():
    query = '''
    SELECT 
        f.departure_airport,
        f.arrival_airport,
        COUNT(t.id) as tickets_sold
    FROM Flights f
    LEFT JOIN Tickets t ON f.id = t.flight_id
    GROUP BY f.departure_airport, f.arrival_airport
    ORDER BY tickets_sold DESC;
    '''
    result = await database.fetchall(query)
    return result
