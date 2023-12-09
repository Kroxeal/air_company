from fastapi import HTTPException

from src.db.models import Flight, Ticket, TicketDetails, PatchTicket, TicketAll, TicketCreate, TicketPatch
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def create_ticket_raw(ticket: TicketCreate):
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
        $1,
        $2,
        $3,
        $4,
        $5,
        $6   
    )
    '''
    values = (
        ticket.flight,
        ticket.user,
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
async def delete_ticket_raw(id):
    query = '''
    DELETE FROM
    tickets
    WHERE
    id = $1
    '''
    values = (
        id,
    )
    await database.execute(query, *values)
    return f'Ticket deleted'


@db_connection
async def get_all_tickets():
    query = '''
    SELECT 
        tickets.*,
        users.name,
        users.surname,
        flights.departure_airport,
        flights.arrival_airport 
    FROM tickets tickets
    INNER JOIN users ON tickets.user_id = users.id
    INNER JOIN flights ON tickets.flight_id = flights.id
    '''
    results = await database.fetchall(query)
    tickets_lst = []
    for result in results:
        tickets_dct = {
            'id': result['id'],
            'flight': result['departure_airport'] + ' ' + result['arrival_airport'],
            'user': result['name'] + ' ' + result['surname'],
            'service_class': result['service_class'],
            'price': result['price'],
            'status': result['status'],
            'booking_date': result['booking_date'],
        }
        tickets_lst.append(TicketAll(**tickets_dct))
    return tickets_lst


@db_connection
async def update_ticket_form_raw(id: str, ticket: TicketPatch):
    query = '''
    UPDATE tickets
    SET
    flight_id = COALESCE($1, flight_id),
    user_id = COALESCE($2, user_id),
    service_class = COALESCE($3, service_class),
    price = COALESCE($4, price),
    status = COALESCE($5, status),
    booking_date = COALESCE($6, booking_date)
    WHERE
    id = $7
    '''
    values = (
        ticket.flight,
        ticket.user,
        ticket.service_class,
        ticket.price,
        ticket.status,
        ticket.booking_date,
        id,
    )
    await database.execute(query, *values)
    return ticket
