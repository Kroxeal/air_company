from src.db.models import TicketAll, TicketsCart, PatchTicket, TicketPatch, CartTicket
from src.db.settings import database
from src.services.decorators.connect_decorator import db_connection


@db_connection
async def get_all_tickets_user(username: str):
    query = '''
    SELECT 
        tickets.*,
        users.name,
        users.surname,
        flights.departure_airport,
        flights.arrival_airport,
        flights.departure_datetime,
        flights.arrival_datetime
    FROM tickets
    INNER JOIN users
    ON tickets.user_id = users.id
    INNER JOIN flights
    ON tickets.flight_id = flights.id
    WHERE users.username = $1
    '''
    values = (
        username,
    )
    results = await database.fetchall(query, *values)
    tickets_lst = []
    for result in results:
        tickets_dct = {
            'id': result['id'],
            'flight': result['departure_airport'] + ' ' + result['arrival_airport'],
            'user': result['name'] + ' ' + result['surname'],
            'service_class': result['service_class'],
            'departure_datetime': result['departure_datetime'],
            'arrival_datetime': result['arrival_datetime'],
            'price': result['price'],
            'status': result['status'],
            'booking_date': result['booking_date'],
        }
        tickets_lst.append(TicketsCart(**tickets_dct))
    return tickets_lst


@db_connection
async def update_ticket_raw(ticket: CartTicket):
    query = '''
    UPDATE tickets
    SET
    flight_id = COALESCE($1, flight_id),
    service_class = COALESCE($2, service_class),
    status = COALESCE($3, status),
    booking_date = COALESCE($4, booking_date),
    price = COALESCE($5, price)
    WHERE
    id = $6
    '''
    values = (
        ticket.flight,
        ticket.service_class,
        ticket.status,
        ticket.booking_date,
        ticket.price,
        ticket.id,
    )
    await database.execute(query, *values)
    return ticket
