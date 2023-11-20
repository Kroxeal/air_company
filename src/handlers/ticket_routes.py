from fastapi import APIRouter

from src.db.models import Ticket, TicketDetails, PatchTicket
from src.services.CRUD.Tickets_crud import create_ticket_raw, get_ticket_raw, get_ticket_details_raw, update_ticket_raw, \
    delete_ticket_raw

router = APIRouter()


@router.post('/', response_model=Ticket)
async def create_ticket(username: str, flight_number: str, ticket: Ticket):
    return await create_ticket_raw(username, flight_number, ticket)


@router.get('/', response_model=Ticket)
async def get_ticket(username: str, flight_number: str):
    return await get_ticket_raw(username, flight_number)


@router.get('/detail/', response_model=TicketDetails)
async def get_ticket_details(username: str, flight_number: str):
    return await get_ticket_details_raw(username, flight_number)


@router.patch('/', response_model=PatchTicket)
async def update_ticket(username: str, flight_number: str, ticket: PatchTicket):
    return await update_ticket_raw(username, flight_number, ticket)


@router.delete('/')
async def delete_ticket(username: str, flight_number: str):
    return await delete_ticket_raw(username, flight_number)
