from fastapi import HTTPException

from src.db.models import Flight, Ticket, TicketDetails, PatchTicket
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_ticket_raw(username: str, flight_number: str, ticket: Ticket):
    query = '''
    INSERT INTO 
    tickets(
    flight_id,
    user_id,
    service_class,
    price,
    status,
    booking_date
    )
    VALUES (
        (SELECT id FROM flights WHERE flight_number = $1),
        (SELECT id FROM users WHERE username = $2),
        $3,
        $4,
        $5,
        $6   
    )
    '''
    values = (
        flight_number,
        username,
        ticket.service_class,
        ticket.price,
        ticket.status,
        ticket.booking_date,
    )
    await database.execute(query, *values)
    return ticket


@db_connection
async def get_ticket_raw(username: str, flight_number: str):
    query = '''
    SELECT * FROM 
    tickets
    WHERE user_id = (
        SELECT id FROM users WHERE username = $1
    )
    AND
    flight_id = (
        SELECT id FROM flights WHERE flight_number = $2
    )
    '''
    values = (
        username,
        flight_number,
    )
    result = await database.fetchrow(query, *values)
    return Ticket(**result)


@db_connection
async def get_ticket_details_raw(username: str, flight_number: str):
    query = '''
        SELECT 
         tickets.*,
         users.username,
         flights.flight_number
        FROM 
        tickets
        LEFT JOIN users ON tickets.user_id = users.id
        LEFT JOIN flights ON tickets.flight_id = flights.id
        WHERE users.username = $1
        AND
        flights.flight_number = $2
    '''
    values = (
        username,
        flight_number,
    )
    result = await database.fetchrow(query, *values)
    if result:
        ticket_data = {
            'flight_id': result['flight_number'],
            'user_id': result['username'],
            'service_class': result['service_class'],
            'price': result['price'],
            'status': result['status'],
            'booking_date': result['booking_date'],
        }
        ticket = TicketDetails(**ticket_data)
        return ticket
    else:
        raise HTTPException(status_code=400, detail="There's no such a Ticket")


@db_connection
async def update_ticket_raw(username: str, flight_number: str, ticket: PatchTicket):
    query = '''
    UPDATE tickets
    SET
    flight_id = COALESCE((SELECT id FROM flights WHERE flight_number = $1), flight_id),
    service_class = COALESCE($2, service_class),
    price = COALESCE($3, price),
    status = COALESCE($4, status),
    booking_date = COALESCE($5, booking_date)
    WHERE
    user_id = (
        SELECT id FROM users WHERE username = $6 
    )
    AND
    flight_id = (
        SELECT id FROM flights WHERE flight_number = $7
    )
    '''
    values = (
        ticket.flight_number,
        ticket.service_class,
        ticket.price,
        ticket.status,
        ticket.booking_date,
        username,
        flight_number,
    )
    await database.execute(query, *values)
    return ticket


@db_connection
async def delete_ticket_raw(username: str, flight_number: str):
    query = '''
    DELETE FROM
    tickets
    WHERE
    user_id = (
        SELECT id FROM users WHERE username = $1 
    )
    AND
    flight_id = (
        SELECT id FROM flights WHERE flight_number = $2
    )
    '''
    values = (
        username,
        flight_number,
    )
    await database.execute(query, *values)
    return f'Ticket name: {username} and flight_number: {flight_number} deleted'
